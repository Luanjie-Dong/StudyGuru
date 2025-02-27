#!/usr/bin/env python3
from supabaseClient import supabase
from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)

CORS(app)

@app.route("/notes", methods=['GET'])
def get_all_notes_for_module():
    """
        PARAMS:
        module_id:a6efb5ac-c0aa-4b81-8541-cfea248f786a
        
        Returns:
        [
            {
                "module_id": "a6efb5ac-c0aa-4b81-8541-cfea248f786a",
                "note_id": "71364235-5489-4d10-aa4f-0c10fc403067",
                "pdf_URL": "www.yahoo.com"
            }
        ]
    """
    
    module_id = request.args.get('module_id')
    if not module_id:
        return jsonify({'Error':'Missing module_id!'}),400
    
    try:
        response = (
            supabase.table('notes')
            .select('*')
            .eq('module_id',module_id)
            .execute())
        if response.data:
            return jsonify(response.data),200
        else:
            return jsonify({'Error':f"Module {module_id} has no notes!"}),404
    except Exception as e:
        return jsonify({"Error":str(e)}),500
    

@app.route("/notes", methods=['POST'])
def add_one_note():
    data = request.get_json()
    '''
        Sample data:
        { 
            "module_id":"a6efb5ac-c0aa-4b81-8541-cfea248f786a",
            "pdf_URL":"www.yahoo.com"
        }
        Returns:
        {
            "Message": "Note added successfully!",
            "note_id": "71364235-5489-4d10-aa4f-0c10fc403067"
        }
    '''
    
    #Validation
    required_fields = {'module_id', 'pdf_URL'}
    if not data or not all(field in data for field in required_fields):
        return jsonify({'Error':'Missing module_id or pdf_URL!'}),400
    #End
    
    module_id = data['module_id']
    pdf_URL = data['pdf_URL']
    insert_data = {"module_id":module_id, "pdf_URL":pdf_URL}

    try:
        response = supabase.table('notes').insert(insert_data).execute()
        print(response)
        if response.data is not None:
            return jsonify({"Message":'Note added successfully!',
                            "note_id":response.data[0]['note_id']}),201
        else: 
            return jsonify({"Error": 'Note not added...'}),500
        
    except Exception as e:
        return jsonify({"Error":str(e)}),500
    
    
@app.route("/notes", methods=['DELETE'])
def delete_one_note():
    '''
        PARAMS:
        note_id:71364235-5489-4d10-aa4f-0c10fc403067
    
        Returns:
        {
            "Message": "Note deleted successfully!"
        }
    '''

    note_id = request.args.get('note_id')
    if not note_id:
        return jsonify({'Error':'Missing note_id!'}),400
    try:
        response = (supabase.table('notes')
                    .delete()
                    .eq('note_id',note_id)
                    .execute())
        print(response.data)
        if response.data!=[]:
            return jsonify({"Message":f'Note {note_id} deleted successfully!'}),201
        else: 
            return jsonify({"Error": f'Note {note_id} not found!'}),404
        
    except Exception as e:
        return jsonify({"Error":str(e)}),500

    

if __name__=='__main__':
    print("This is flask for " + os.path.basename(__file__) + ": notes ...")
    app.run(debug=True)
