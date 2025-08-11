Webis Frontend API Documentation
=================================

---

1. Upload and Process HTML Files (Synchronous)
----------------------------------------------

**Endpoint**: ``POST /api/process-html``

**Parameters (form-data)**

+-------------+----------+--------+--------------------------------+
| Name        | Type     | Required | Description                    |
+=============+==========+========+================================+
| files       | File[]   | Yes    | List of HTML files              |
+-------------+----------+--------+--------------------------------+
| tag_probs   | File     | No     | Tag probability file            |
+-------------+----------+--------+--------------------------------+
| model_type  | string   | No     | Model type, default is "node"   |
+-------------+----------+--------+--------------------------------+

**Response Example**::

    {
      "task_id": "123456",
      "status": "completed",
      "result_count": 2,
      "message": "Processed successfully",
      "error": null
    }

---

2. Upload and Process HTML Files (Asynchronous)
------------------------------------------------

**Endpoint**: ``POST /api/process-async``

**Parameters (form-data)**  
Same as above.

**Response Example**::

    {
      "task_id": "123456",
      "status": "pending",
      "result_count": 0,
      "message": "Task submitted, processing in the background",
      "error": null
    }

---

3. Query Task Status
--------------------

**Endpoint**: ``GET /api/tasks/{task_id}``

**Path Parameters**
- ``task_id``: Task ID

**Response Example**::

    {
      "status": "completed",
      "message": "Processing completed",
      "output_dir": "/path/to/output",
      "results": [ ... ],
      "error": null,
      "url": null,
      "title": null
    }

---

4. Download Processing Results
------------------------------

**Endpoint**: ``GET /api/tasks/{task_id}/download``

**Path Parameters**
- ``task_id``: Task ID

**Response**
- Downloads a zip file containing the processing results.

---

5. Delete Task
--------------

**Endpoint**: ``DELETE /api/tasks/{task_id}``

**Path Parameters**
- ``task_id``: Task ID

**Response Example**::

    {
      "message": "Task and related files have been deleted"
    }

---

6. Process Webpage via URL
--------------------------

**Endpoint**: ``POST /api/process-url``

**Parameters (form-data or JSON)**

+-------------+----------+--------+--------------------------------+
| Name        | Type     | Required | Description                    |
+=============+==========+========+================================+
| url         | string   | Yes    | Webpage URL                     |
+-------------+----------+--------+--------------------------------+
| model_type  | string   | No     | Model type, default is "node"   |
+-------------+----------+--------+--------------------------------+

**Response Example**  
Same as the "Upload and Process HTML Files" response.

---

7. Fetch Webpage Content via URL
--------------------------------

**Endpoint**: ``GET /api/fetch-url``

**Query Parameters**

+----------------+----------+--------+----------------------------------------------+
| Name           | Type     | Required | Description                                  |
+================+==========+========+==============================================+
| url            | string   | Yes    | Webpage URL                                   |
+----------------+----------+--------+----------------------------------------------+
| remove_scripts | boolean  | No     | Whether to remove scripts, default is true   |
+----------------+----------+--------+----------------------------------------------+
| remove_images  | boolean  | No     | Whether to remove images, default is true    |
+----------------+----------+--------+----------------------------------------------+

**Response**
- Depending on backend implementation, returns webpage content or JSON.

---

Common Response Field Descriptions
-----------------------------------

+--------------+----------------------------------------------+
| Field        | Description                                  |
+==============+==============================================+
| task_id      | Task ID                                       |
+--------------+----------------------------------------------+
| status       | Task status (pending/completed/failed)        |
+--------------+----------------------------------------------+
| result_count | Number of results                             |
+--------------+----------------------------------------------+
| message      | Status message                                |
+--------------+----------------------------------------------+
| error        | Error message                                 |
+--------------+----------------------------------------------+
| results      | Result content                                |
+--------------+----------------------------------------------+

---

For detailed field descriptions, frontend code examples, or API integration support, please feel free to contact us.


API Usage Examples
====================

This page explains how to use the API interfaces provided by Webis for structured information extraction, suitable for client programs or scripts with raw HTML data.

Example script: ``samples/api_usage.py``

The script demonstrates two typical calling patterns:

- Synchronous processing: Suitable for small batches of data, where the client waits for the response
- Asynchronous processing: Suitable for large batches of files, processed in the background with status polling capability

-----------------------------

Synchronous Processing Mode
-----------------------------

Used for one-time upload of a single or a small number of HTML files, with immediate waiting for extraction results:

.. code-block:: python

   import requests

   files = {"file": open("input.html", "rb")}
   data = {"task_id": "demo-task"}

   # Submit HTML for synchronous processing
   response = requests.post(
       "http://localhost:8002/extract/process-html",
       files=files,
       data=data
   )

   print("Processing result:", response.json())

   # Download compressed results
   task_id = data["task_id"]
   download_response = requests.get(
       f"http://localhost:8002/tasks/{task_id}/download", stream=True
   )
   with open(f"{task_id}_results.zip", "wb") as f:
       for chunk in download_response.iter_content(chunk_size=8192):
           f.write(chunk)

-----------------------------

Asynchronous Processing Mode
-----------------------------

Suitable for background processing, large file uploads and other scenarios, the interface returns an asynchronous task ID:

.. code-block:: python

   import requests

   files = {"file": open("input.html", "rb")}
   data = {"task_id": "long-task"}

   # Submit asynchronous task
   response = requests.post(
       "http://localhost:8002/extract/process-async",
       files=files,
       data=data
   )

   async_task_id = response.json()["task_id"]

   # Query task status
   status = requests.get(f"http://localhost:8002/tasks/{async_task_id}")
   print("Current status:", status.json())

   # Download processing results (after completion)
   download_response = requests.get(
       f"http://localhost:8002/tasks/{async_task_id}/download", stream=True
   )
   with open(f"{async_task_id}_async_results.zip", "wb") as f:
       for chunk in download_response.iter_content(chunk_size=8192):
           f.write(chunk)

-----------------------------

Running Example Scripts
-----------------------------

Use the built-in example script ``samples/api_usage.py`` to run test calls:

.. code-block:: bash

   # Default call to local service (synchronous mode)
   python samples/api_usage.py

   # Using DeepSeek or other remote API (requires API key)
   python samples/api_usage.py --use-deepseek --api-key YOUR_API_KEY_HERE

Result explanation:

- Synchronous task: Saved as ``{task_id}_results.zip``
- Asynchronous task: Saved as ``{async_task_id}_async_results.zip``

Ensure that there is at least one HTML file in the ``input_html/`` directory.
