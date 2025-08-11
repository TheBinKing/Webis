Performance Optimization Guide
==============================

.. note::
   This guide provides tips for optimizing the performance of **Webis** when
   running locally or on a cloud server.  
   Since Webis is powered by vLLM and large language models, both **GPU memory**
   and **CPU throughput** can greatly affect performance.

Hardware Recommendations
------------------------

- **GPU**: NVIDIA GPU with CUDA support
  - Recommended: ≥ 8GB VRAM
  - Minimum: 6GB VRAM (requires lowering ``--memory-limit`` and precision)
- **CPU**: ≥ 4 physical cores
- **RAM**: ≥ 16GB
- **Disk**: SSD storage for faster model loading

GPU Memory Optimization
-----------------------

1. Adjust GPU memory utilization
   - By default, vLLM uses 90% of available GPU memory.
   - Lower it if VRAM is limited::

        python scripts/start_model_server.py --memory-limit 0.6

2. Use lower precision
   - ``float16``: Reduces memory usage significantly, with minor accuracy loss.
   - ``int8`` quantization: Further reduces memory usage, but may reduce quality.

   Example (modify model loading in ``start_model_server.py``)::

        model = LLM(
            model=model_path,
            tensor_parallel_size=1,
            gpu_memory_utilization=gpu_memory_utilization,
            trust_remote_code=True,
            dtype="float16"
        )

3. Free GPU memory before starting
   - List and kill unnecessary GPU processes::

        nvidia-smi
        kill -9 <PID>

CPU & Concurrency Tuning
------------------------

1. Increase request concurrency
   - Use ``--host 0.0.0.0`` to allow LAN access.
   - Run multiple workers with ``uvicorn``::

        uvicorn scripts.start_model_server:app --host 0.0.0.0 --port 8000 --workers 2

2. Batch requests where possible
   - vLLM benefits from batch processing multiple prompts at once.
   - Consider merging small requests into one API call.

Disk & Model Loading
--------------------

1. Cache models locally
   - Avoid repeated downloads by ensuring HuggingFace cache is preserved::

        ~/.cache/huggingface/hub

2. Use SSD storage
   - Model loading speed is much faster on SSD compared to HDD.

Network Optimization
--------------------

1. For cloud servers, choose regions close to your users.
2. Use a reverse proxy (e.g., Nginx) for handling HTTP keep-alive connections.
3. Enable compression (gzip) for API responses if they are large.

Common Optimization Scenarios
-----------------------------

- **Low VRAM GPU (6GB)**:
  - ``--memory-limit 0.6``
  - ``dtype="float16"``
  - Reduce ``max_tokens`` in API requests

- **High concurrency API**:
  - Increase ``uvicorn`` workers
  - Use batching

- **Slow model loading**:
  - Keep the server running (avoid frequent restarts)
  - Store models on SSD

Troubleshooting
---------------

- **"No available memory for cache blocks"**:
  Lower ``--memory-limit`` or free GPU memory.
- **"Free memory on device ... less than desired"**:
  Reduce GPU memory utilization or close other GPU processes.
- **"CUDA not found"**:
  Install NVIDIA drivers and CUDA toolkit properly.
