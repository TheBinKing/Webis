# Webis HTML Content Processing Example

This directory contains example code for processing HTML files using the Webis system. The Webis system provides two main usage methods: API interface and Command Line Interface (CLI), and supports integration with popular HTML content extraction tools such as goose3, newspaper3k, and trafilatura.

## 一. API Usage Examples

The api_usage.py script demonstrates how to process HTML files via the API interface, supporting both synchronous and asynchronous processing modes:

### 1. Synchronous Processing Mode

Synchronous processing is suitable for a small number of afiles, where the client needs to wait for the server to complete processing. The process is as follows:

- Send the HTML file to the server
- Wait for processing to complete
- Directly obtain the processing results
- Save the results to a compressed package

Example code:

```python
import requests

# Process HTML file synchronously
with open('input_html/sample.html', 'rb') as file:
    response = requests.post(
        "http://localhost:8002/extract/process-html",
        files={'file': file},
        data={'extractor': 'trafilatura'}  # Example parameter
    )

# Save results
task_id = response.json()['task_id']
with requests.get(f"http://localhost:8002/tasks/{task_id}/download", stream=True) as r:
    with open(f"{task_id}_results.zip", 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
```
### 2. Asynchronous Processing Mode

Asynchronous processing is suitable for a large number of files or scenarios requiring long processing times. The process is as follows:

- Submit the HTML file to the server to start an asynchronous task
- Periodically check the task status
- Obtain the results after the task is completed
- Save the results to another compressed package

Example code:

```python
import requests
import time

# Initiate async task
with open('input_html/sample.html', 'rb') as file:
    response = requests.post(
        "http://localhost:8002/extract/process-async",
        files={'file': file},
        data={'enhance': 'true'}  # Example parameter
    )

# Monitor progress
async_task_id = response.json()['task_id']
while requests.get(f"http://localhost:8002/tasks/{async_task_id}").json()['status'] != 'completed':
    time.sleep(5)

# Retrieve results
with requests.get(f"http://localhost:8002/tasks/{async_task_id}/download", stream=True) as r:
    with open(f"{async_task_id}_async_results.zip", 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
```
### Running the API Example
```bash
# Basic execution
python api_usage.py

# With DeepSeek enhancement
python api_usage.py --use-deepseek --api-key YOUR_API_KEY_HERE

# Specify extractor
python api_usage.py --extractor newspaper3k
```
## 二. Command Line Interface (CLI) Usage Examples

The cli_usage.sh script demonstrates how to process HTML files using the command line interface. The CLI provides a simpler batch processing method, suitable for integration into automated scripts.

### Basic Usage Method
```bash
# Process HTML files
webis extract \
    --input /path/to/input_html \
    --output /path/to/output_basic \
    --use-deepseek \
    --verbose
```

### Utility Commands
```bash
# View version information
webis version

# Check API connection
webis check-api --api-key YOUR_API_KEY

# View help
webis --help
webis extract --help
```
## File Descriptions
- api_usage.py: API interface usage example
- cli_usage.sh: Command line interface usage example
- input_html/: Directory for example HTML files
- output_basic/: Directory for CLI output results
- requirements.txt: List of dependency packages (including requests, goose3, newspaper3k, trafilatura, etc.)

## Processing Results Description

When processing HTML files using the API, a compressed package is generated, with contents varying based on the processing mode and tool used:

1. Synchronous processing results {task_id}_results.zip: Contains the results of HTML files processed via the synchronous API (first 2 files)

2. Asynchronous processing results {async_task_id}_async_results.zip: Contains the results of HTML files processed via the asynchronous API (3rd file)

The compressed package includes the following contents:
- Preprocessed HTML content
- Dataset file
- Model prediction results
- Processed text content


## Notes
1. Server Startup: Ensure the following servers are running:

- Model server (port 8000) [started]
- Web API server (port 8002) [running] 
Example startup command: python -m uvicorn app:app --host 0.0.0.0 --port 8002

2. DeepSeek Enhancement Requires a Valid API Key: Key configuration method: export DEEPSEEK_API_KEY=YOUR_API_KEY_HERE or specify --api-key in the command

3. Dependency Installation:
Install required Python packages: pip install -r requirements.txt

4. File Paths: 
After processing, results are saved in the script execution directory by default. It is recommended to specify the --output parameter to avoid overwriting.

5. Performance Optimization:
- For large files, prioritize asynchronous processing mode.
- Adjust batch_size (in CLI, use --batch-size) to optimize memory usage.