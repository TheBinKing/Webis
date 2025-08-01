#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
import json
import time
from pathlib import Path
import sys
import argparse

def main(use_deepseek=False, api_key=None):
    print("1. Checking API server status")
    try:
        response = requests.get("http://localhost:8002/")
        if response.status_code == 200:
            print("✓ API server is running")
        else:
            print(f"× API server returned error: {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print("× API server not running, please start server.py first")
        print("  Hint: Run 'python src/web_extractor/server.py' to start the server")
        return

    print("\n2. Checking model server status")
    response = requests.get("http://localhost:8002/check-model-server")
    if response.json().get("status") == "online":
        print("✓ Model server is running")
    else:
        print("× Model server not running or unreachable")
        print("  Hint: Please ensure node_model_server.py is running")
        return

    html_files_dir = Path(r"/data0/ziyan_full/llm_extra/webflow_github/Webis/samples/input_html")
    if not html_files_dir.exists() or not any(html_files_dir.glob("*.html")):
        print(f"\n× No HTML test files found, please ensure {html_files_dir} contains HTML files")
        return
    
    html_files = list(html_files_dir.glob("*.html"))
    print(f"\n3. Found {len(html_files)} HTML files to process")
    for i, file in enumerate(html_files):
        print(f"  {i+1}. {file.name}")
    
    if use_deepseek and not api_key:
        print("\n× Error: DeepSeek API key required when using DeepSeek")
        return

    print("\n4. Processing HTML files synchronously")
    if use_deepseek:
        print("  Using DeepSeek API for additional content optimization")
    
    files = []
    for html_file in html_files[:2]:
        files.append(("files", (html_file.name, open(html_file, "rb"), "text/html")))
    
    data = {"model_type": "node"}
    
    if use_deepseek:
        data["use_deepseek"] = "true"
        data["api_key"] = api_key
    
    response = requests.post(
        "http://localhost:8002/extract/process-html",
        files=files,
        data=data
    )
    
    for _, (_, file_obj, _) in files:
        file_obj.close()
    
    if response.status_code == 200:
        result = response.json()
        task_id = result.get("task_id")
        print(f"✓ Processing successful, Task ID: {task_id}")
        print(f"  Number of results: {result.get('result_count')}")
        
        print("\n5. Getting task details")
        response = requests.get(f"http://localhost:8002/tasks/{task_id}")
        if response.status_code == 200:
            task_details = response.json()
            print(f"  Task status: {task_details.get('status')}")
            
            if task_details.get("results"):
                print("\n6. Results preview:")
                for i, result_file in enumerate(task_details["results"][:2]):
                    print(f"\nResult {i+1}: {result_file['filename']}")
                    print(f"  Source: {result_file['source']}")
                    content_preview = result_file['content'][:200]
                    print(f"  {content_preview}...")
                
                print("\n7. Downloading all results")
                response = requests.get(f"http://localhost:8002/tasks/{task_id}/download", stream=True)
                if response.status_code == 200:
                    zip_file = f"{task_id}_results.zip"
                    with open(zip_file, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    print(f"✓ Results saved to {zip_file}")
                else:
                    print(f"× Failed to download results: {response.status_code}")
            else:
                print("No results found")
        else:
            print(f"× Failed to get task details: {response.status_code}")
    else:
        print(f"× Processing failed: {response.status_code}")
        print(response.text)

    print("\n8. Processing HTML files asynchronously")
    if use_deepseek:
        print("  Using DeepSeek API for additional content optimization")
        
    files = []
    for html_file in html_files[2:4]:
        if html_file.exists():
            files.append(("files", (html_file.name, open(html_file, "rb"), "text/html")))
    
    if files:
        data = {"model_type": "node"}
        
        if use_deepseek:
            data["use_deepseek"] = "true"
            data["api_key"] = api_key
        
        response = requests.post(
            "http://localhost:8002/extract/process-async",
            files=files,
            data=data
        )
        
        for _, (_, file_obj, _) in files:
            file_obj.close()
        
        if response.status_code == 200:
            async_task_id = response.json().get("task_id")
            print(f"✓ Async task submitted, Task ID: {async_task_id}")
            
            print("\n9. Monitoring async task status")
            max_attempts = 30  # 增加到30次检查，每次5秒，总共最多等待150秒
            for i in range(max_attempts):
                print(f"  Checking... ({i+1}/{max_attempts})")
                response = requests.get(f"http://localhost:8002/tasks/{async_task_id}")
                if response.status_code != 200:
                    print(f"  Error getting task status: {response.status_code}")
                    time.sleep(5)
                    continue
                
                task_data = response.json()
                status = task_data.get("status")
                print(f"  Current status: {status}")
                
                if status == "completed":
                    print("✓ Async task completed")
                    print(f"  Used DeepSeek: {task_data.get('used_deepseek', False)}")
                    
                    # 如果有结果，显示结果预览
                    results = task_data.get("results", [])
                    if results:
                        print(f"\n10. Found {len(results)} result files")
                        for i, result in enumerate(results[:2]):  # 最多显示前2个结果
                            print(f"\nResult {i+1}: {result.get('filename', 'unknown')}")
                            print(f"  Source: {result.get('source', 'unknown')}")
                            content = result.get('content', '')
                            content_preview = content[:200] if content else 'No content'
                            print(f"  {content_preview}...")
                        
                        # 下载结果
                        print("\n11. Downloading async task results")
                        download_response = requests.get(f"http://localhost:8002/tasks/{async_task_id}/download", stream=True)
                        if download_response.status_code == 200:
                            zip_file = f"{async_task_id}_async_results.zip"
                            with open(zip_file, 'wb') as f:
                                for chunk in download_response.iter_content(chunk_size=8192):
                                    f.write(chunk)
                            print(f"✓ Results saved to {zip_file}")
                        else:
                            print(f"× Failed to download async results: {download_response.status_code}")
                    else:
                        print("No results found in completed task")
                    break
                    
                elif status == "failed":
                    print(f"× Async task failed: {task_data.get('error', 'Unknown error')}")
                    break
                
                time.sleep(5)
        else:
            print(f"× Failed to submit async task: {response.status_code}")
            print(response.text)
    else:
        print("Not enough HTML files found for async processing example")

    print("\nExample run completed!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web Content Extraction Example")
    parser.add_argument("--use-deepseek", "-d", action="store_true", 
                      help="Whether to use DeepSeek to optimize extraction results")
    parser.add_argument("--api-key", "-k", type=str, 
                      help="DeepSeek API key")
    
    args = parser.parse_args()
    
    main(use_deepseek=args.use_deepseek, api_key=args.api_key)