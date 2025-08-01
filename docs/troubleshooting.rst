Troubleshooting Guide
=================================

This page lists common errors and solutions encountered while using Webis.

---

Unable to Access API: 401 Unauthorized
-------------------------------

**Cause**:

- No valid API Key provided, or server authentication is enabled.

**Solution**:

- Check ``api_keys.json`` in the project root directory and copy a valid key.
- Add the ``api_key`` parameter when calling the API, for example:

  .. code-block:: bash

     curl -X POST http://localhost:8000/generate \
       -H "Content-Type: application/json" \
       -d '{"prompt": "hello", "api_key": "your-key"}'

---

Model Loading Failed Due to Insufficient GPU Memory
-------------------------------

**Error**:

.. code-block:: text

   ValueError: Free memory on device (...) is less than desired GPU memory utilization (...)

**Cause**:

- Remaining GPU memory is less than the model's required usage limit.

**Solution**:

- Set a lower ``GPU_MEMORY_UTILIZATION``:

  .. code-block:: bash

     export GPU_MEMORY_UTILIZATION=0.6

---

libcudart.so Not Found Error
--------------------------

.. code-block:: text

   ImportError: libcudart.so.11.0: cannot open shared object file: No such file or directory

**Cause**:

- CUDA dynamic library not installed or version incompatible.

**Solution**:

- Install PyTorch with corresponding CUDA through conda:

  .. code-block:: bash

     conda install pytorch-cuda=12.1 -c pytorch -c nvidia

---

Build Failed: C Compiler Not Found
--------------------------

.. code-block:: text

   RuntimeError: Failed to find C compiler.

**Cause**:

- Compiler tools like ``gcc`` not found when Triton is compiling model kernels.

**Solution**:

- Install ``build-essential``:

  .. code-block:: bash

     sudo apt update
     sudo apt install build-essential

---

HuggingFace Model Download Failed (WSL Network Issue)
-------------------------------------------

**Symptoms**:

- Model download gets stuck or reports `ConnectionError`, `Failed to establish new connection`

**Solution**:

1. Open CMD in Windows and run:

   .. code-block:: cmd

      ipconfig

2. Find your machine's IPv4 address, e.g., `192.168.0.123`

3. Set proxy in WSL:

   .. code-block:: bash

      export http_proxy=http://192.168.0.123:7890
      export https_proxy=http://192.168.0.123:7890

---

No Model Output / API Returns Empty String
------------------------------

**Possible Causes**:

- ``prompt`` content incomplete or lacking context.
- ``max_tokens`` set too low, generation truncated.

**Suggestions**:

- Increase the ``max_tokens`` parameter appropriately (e.g., 256 → 512)
- Use clear prompts, for example:

  .. code-block:: text

     Please extract contact name and phone number from the following HTML: <html>...</html>

---

Package Manager Lock Error (dpkg/apt)
------------------------------

**Error**:

.. code-block:: text

   Waiting for cache lock: Could not get lock /var/lib/dpkg/lock-frontend. It is held by process

**Cause**:

- Another package management process (apt, apt-get, dpkg, or system update) is running
- A previous package installation was interrupted, leaving a lock file

**Solution**:

1. Wait if another legitimate update is in progress
2. If no other update is running, check for the process holding the lock:

   .. code-block:: bash

      ps aux | grep -i apt

3. If needed, remove the lock files (use with caution):

   .. code-block:: bash

      sudo rm /var/lib/apt/lists/lock
      sudo rm /var/lib/dpkg/lock
      sudo rm /var/lib/dpkg/lock-frontend
      sudo dpkg --configure -a