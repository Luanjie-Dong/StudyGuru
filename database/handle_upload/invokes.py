import requests
import io

SUPPORTED_HTTP_METHODS = set([
     "GET", "OPTIONS", "HEAD", "POST", "PUT", "PATCH", "DELETE"
])

def invoke_http(url, method='GET', json=None, files=None, data=None, params=None, **kwargs):
     """A wrapper for requests methods to handle HTTP calls, including file uploads and JSON as form data.
       url: the URL of the HTTP service;
       method: the HTTP method;
       json: JSON data to send (for JSON payloads);
       files: file object or dictionary of files to upload (for multipart/form-data);
       data: dictionary or string of form data (e.g., JSON string or module_id) to send with files;
       return: the JSON reply content from the HTTP service if successful;
               otherwise, return a JSON object with a "code" name-value pair.
    """
     code = 200
     result = {}

     try:
          if method.upper() not in SUPPORTED_HTTP_METHODS:
               raise Exception(f"HTTP method {method} unsupported.")

          # Handle file upload for POST or PUT methods. 
          ## If file sent tgt, use files + data. Else, use json.
          if method.upper() in ["POST", "PUT"]:
               if files is not None:
                    # Prepare form data
                    form_data={}
                    if data:
                         if isinstance(data, dict):
                              # If data is a dictionary, use its key-value pairs directly as form fields
                              form_data.update(data)
                         else:
                              raise Exception("Invalid data format. Use dict or JSON string for form data.")

                    # Send the request with both files and form data
                    files_content = files.read()  # Read the binary content of the FileStorage object
                    files_obj = io.BytesIO(files_content)  # Create a BytesIO object for streaming

                    # Send via invoke_http
                    files_data = {'file': (files.filename, files_obj, files.content_type)}  # Tuple with filename, file object, and content type
                    print('Files_data sent from invokes.py:',files_data)
                    print('Data sent from invokes.py:', form_data)
                    r = requests.request(method.upper(), url, files=files_data, data=form_data, **kwargs)
               else:
                    # If no files, use JSON data
                    if json is not None:
                         print('json sent by invokes.py:', json)
                         r = requests.request(method.upper(), url, json=json, **kwargs)
                    else:
                         raise Exception("No data or files provided for POST/PUT request.")
          else:
          # For GET, DELETE, etc., use params for query parameters
               if params is not None:
                    if not isinstance(params, dict):
                         raise Exception("Params must be a dictionary for query parameters.")
                    # Send the request with query parameters
                    print('params sent by invokes.py:', params)
                    r = requests.request(method.upper(), url, params=params, **kwargs)
               else:
                    # No params, send a simple request
                    print('simple get request with no params sent')
                    r = requests.request(method.upper(), url, **kwargs)
          result=r.json()
     except Exception as e:
          code = 500
          result = {"code": code, "message": "invocation of service fails: " + url + ". " + str(e)}

     return result

