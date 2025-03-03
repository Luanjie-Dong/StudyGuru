#!/usr/bin/env python3
from flask import Flask, jsonify, request
from flask_cors import CORS
from invokes import invoke_http
import os
from threading import Thread

app = Flask(__name__)

CORS(app)

storage_url = "http://storage:5000/upload" #POST
ocr_url = "http://llm:5000/generate_topics" #POST
notes_API_url = "http://notes:5000/notes" #POST

@app.route("/handle_upload", methods=['POST'])
def handle_upload():
    """
    FORM DATA:
    module_id: 06ba3cc9-c8e5-4294-8e78-21cc6c7097d4
    course_id: 6f1cc9d6-d8ac-49d6-8849-8d3d4f4c9d98
    file: [file] (see postman)

    RETURNS:
    {
        "Message": "All files uploaded!",
        "uploaded_files": [
            {
                "filename": "Post_Incident_Report.pdf",
                "url": "https://lulvcodujqpxgvhkzyfc.supabase.co/storage/v1/object/public/notes/06ba3cc9-c8e5-4294-8e78-21cc6c7097d4/Post_Incident_Report.pdf?"
            }
        ]
    }
    """
    try:
        module_id = request.form.get('module_id')
        course_id = request.form.get('course_id')
        if not module_id or not course_id:
            return jsonify({'error': 'Missing module_id or course_id'}), 400

        # Check if a file is present in the request
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400
        
        files = request.files['file']
        
        # Check if a file was actually selected
        if files.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        print("File received, processing file upload now...",flush=True)
        print(f"\nInvoking storage microservice...",flush=True)
        data={"module_id":module_id}
        storage_result = invoke_http(storage_url, method="POST", files=files, data=data)
        print(f"storage_result: {storage_result}\n",flush=True)
        if storage_result.get('error',False):
            return storage_result,400
        if storage_result.get('code',False):
            return jsonify({'error':storage_result['message']}),storage_result['code']
        note_URL = storage_result["uploaded_files"][0]['url']
        print('Trigerring backend ocr and notes services in background...',flush=True)
        Thread(target=handleNoteUpload,args=(note_URL,module_id,course_id)).start()
        return storage_result,202
        
    except KeyError as e:
        return jsonify({'error':'Key Error. Invalid key passed.',
                        'details':f'Key not found: {str(e)}'}),400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


def handleNoteUpload(note_URL, module_id, course_id):
    if not note_URL or not module_id or not course_id:
        return print("error: Missing note_URL, module_id or course_id", flush=True)
    
    try:
        print(f"\nInvoking OCR microservice...",flush=True)
        ocr_json_data = {"note_URL":note_URL,"module_id":module_id, "course_id":course_id}
        ocr_result = invoke_http(ocr_url,'POST',json=ocr_json_data)
        print(f"ocr_result:{ocr_result}\n", flush=True)
        topics = ocr_result
        # topics=[]

        print(f"\nInvoking notes microservice...",flush=True)
        notes_json_data = {"module_id":module_id, "note_URL":note_URL, "topics":topics}
        notes_result = invoke_http(notes_API_url, "POST", json=notes_json_data)
        print(f"notes_result:{notes_result}\n",flush=True)
        if notes_result.get('Error',False):
            print('error:',notes_result,flush=True)
            raise Exception("An error occured with notes microservices.")

        print(f"Message:Backend tasks to ocr and notes successful\n",flush=True)
    except Exception as e:
        print('error',str(e),flush=True)



if __name__=='__main__':
    print("This is flask for " + os.path.basename(__file__) + ": handle_upload ...",flush=True)
    app.run(host='0.0.0.0',debug=True, port=5000)

