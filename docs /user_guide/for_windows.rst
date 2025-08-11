Windows + WSL Quickstart Guide
==============================

.. note::
   This guide is for Windows users who want to deploy and run **Webis** inside
   **WSL (Windows Subsystem for Linux)**.  
   Since vLLM only supports Linux, running it directly on native Windows is not
   possible — you must use WSL.  
   We recommend **at least 8GB of VRAM** for local deployment. If your GPU has
   less VRAM, consider using a cloud server.

Environment Setup
-----------------

1. Check your GPU and drivers
   - Make sure **NVIDIA Driver (version >= 530)** is installed and supports CUDA.
   - Recommended VRAM: **≥ 8GB**, minimum 6GB (requires lowering GPU memory usage).

2. Enable WSL and Virtual Machine Platform
   Open PowerShell **as Administrator** and run::

      dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
      dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

   Then restart your PC.

3. Install WSL and Ubuntu
   - Install the latest version of WSL::

      wsl --install

   - Install Ubuntu (recommended: 20.04 or 22.04)::

      wsl --install -d Ubuntu-22.04

   - Set default WSL version to 2::

      wsl --set-default-version 2

4. Enable GPU support
   - Follow NVIDIA’s official documentation to install **CUDA Toolkit for WSL**.
   - Inside WSL, verify GPU availability::

      nvidia-smi

Installation & Configuration
----------------------------

1. Update packages::

      sudo apt update && sudo apt upgrade -y

2. Install Miniconda (recommended)::

      wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
      bash Miniconda3-latest-Linux-x86_64.sh

   After installation, close and reopen the WSL terminal.

3. Create a Python virtual environment::

      conda create -n webis python=3.10 -y
      conda activate webis

4. Clone the Webis repository::

      git clone https://github.com/<your-repo>/webis.git
      cd webis

5. Install dependencies::

      pip install -r requirements.txt

Model Download & Running
------------------------

1. The default model is::

      Easonnoway/Web_info_extra_1.5b

   On first run, it will be downloaded from HuggingFace into::

      ~/.cache/huggingface/hub

   If your network is slow, consider downloading the model manually and specify the local path when starting.

2. Start the model server::

      python scripts/start_model_server.py --memory-limit 0.8

   If VRAM is insufficient, lower the memory limit::

      python scripts/start_model_server.py --memory-limit 0.6

3. Verify server status
   Open your browser and visit::

      http://127.0.0.1:8000/health

   You should see::

      {"status": "ok", "model": "WebFLow-Node-1.5b"}

API Usage Example
-----------------

Synchronous request::

    import requests

    resp = requests.post(
        "http://127.0.0.1:8000/generate",
        json={"prompt": "Hello", "max_tokens": 50}
    )
    print(resp.json())

For asynchronous usage, see ``samples/api_usage.py``.

Troubleshooting
---------------

- **VRAM insufficient error**:
  Lower the ``--memory-limit`` parameter, or kill other GPU processes::

      nvidia-smi
      kill -9 <PID>

- **HuggingFace download fails**:
  Configure a proxy or use a mirror site; alternatively, download the model manually.

- **CUDA not found**:
  Make sure the NVIDIA driver is installed and ``nvidia-smi`` works inside WSL.
