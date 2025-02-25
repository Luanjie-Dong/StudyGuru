#!/usr/bin/env python3
from supabaseClient import supabase
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

CORS(app)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'pdf', 'pptx', 'bmp', 'tiff'}

# Check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_files():
    """
    Uploads files to supabase storage.
    Storing convention: module_id/filename
    
    Sample Data:
    [CHECK POSTMAN. SEND AS FORM-DATA]

    Returns:
    {
    "Message": "All files uploaded!",
    "Uploaded Files:": [
        {
            "filename": "IS215_project.pdf",
            "url": "https://lulvcodujqpxgvhkzyfc.supabase.co/storage/v1/object/public/notes/bbb42c16-ada0-4d4a-abde-10068bf0a1f2/IS215_project.pdf?"
        }
        ]
    }
    """
    # Check if module_id is in the form data
    if 'module_id' not in request.form:
        return jsonify({"error": "module_id missing."}), 400
    module_id = request.form['module_id']

    # Check if a file is in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    files = request.files.getlist('file')  # Use getlist to handle multiple files
    # Check if any files were selected
    if not files or all(file.filename == '' for file in files):
        return jsonify({'error': 'No files selected'}), 400
    
    uploaded_files = []

    try:        
        # Process each file
        for file in files:
            if file and allowed_file(file.filename):
                # Secure the filename
                filename = secure_filename(file.filename)
                filepath=f'{module_id}/{filename}'
                
                # Read the file data
                file_data = file.read()
                
                # Upload to Supabase Storage
                response = supabase.storage.from_('notes').upload(
                    path=filepath,
                    file=file_data,
                )
                
                # Get public URL of the uploaded file
                public_url = supabase.storage.from_('notes').get_public_url(filepath)
                
                uploaded_files.append({
                    'filename': filename,
                    'url': public_url
                })
            else:
                return jsonify({'error': f'Invalid file type: {file.filename}. Only the following file types are allowed:{ALLOWED_EXTENSIONS}'}), 400
            
        return jsonify({'Message':"All files uploaded!",
                        'Uploaded Files:':uploaded_files}),200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


if __name__=='__main__':
    print("This is flask for " + os.path.basename(__file__) + ": storage ...")
    app.run(debug=True)