#!/usr/bin/env python3
from supabaseClient import supabase
from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)

CORS(app)

@app.route("/notes", methods=['GET'])
def get_all_notes_for_course():
    data = request.get_json()
    """
        Sample data:
        {
            "userid":"502a0caa-8812-424f-9490-eb73f2722ac0",
            "course_name":"ESD"
        }
        Returns:
        [
            {
                "embedding": null,
                "pdf_URL": "www.google.com"
            }
        ]
    """
    if not data or 'userid' not in data or 'course_name' not in data:
        return jsonify({'Error':'Missing userid or course_name'}),400
    
    userid = data['userid']
    course_name = data['course_name']
    try:
        response = (
            supabase.table('notes')
            .select('pdf_URL','embedding')
            .eq('userid',userid)
            .eq('course_name',course_name)
            .execute())
        if response.data:
            return jsonify(response.data),200
        else:
            return jsonify({'Error':"User has no notes!"}),404
    except Exception as e:
        return jsonify({"Error":str(e)}),500
    

@app.route("/notes", methods=['POST'])
def add_one_note():
    data = request.get_json()
    '''
        Sample data:
        { 
            "userid":"502a0caa-8812-424f-9490-eb73f2722ac0",
            "course_name":"ESD",
            "pdf_URL":"www.yahoo.com"
        }
        Returns:
        {
            "Message": "Note added successfully!"
        }
    '''
    
    #Validation
    required_fields = {'userid', 'course_name', 'pdf_URL'}
    if not data or not all(field in data for field in required_fields):
        return jsonify({'Error':'Missing userid, course_name or pdf_URL'}),400
    #End
    
    userid = data['userid']
    course_name = data['course_name']
    pdf_URL = data['pdf_URL']
    insert_data = {"userid":userid, "course_name":course_name, "pdf_URL":pdf_URL} #MISSING EMBEDDINGS FOR NOW

    try:
        response = supabase.table('notes').insert(insert_data).execute()
        print(response)
        if response.data is not None:
            return jsonify({"Message":'Note added successfully!'}),201
        else: 
            return jsonify({"Error": 'Note not added...'}),500
        
    except Exception as e:
        return jsonify({"Error":str(e)}),500
    
    
@app.route("/notes", methods=['DELETE'])
def delete_one_note():
    data = request.get_json()
    '''
        Sample data:
        { 
            "userid":"502a0caa-8812-424f-9490-eb73f2722ac0",
            "course_name":"ESD",
            "pdf_URL":"www.yahoo.com"
        }
        Returns:
        {
            "Message": "Note deleted successfully!"
        }
    '''
    
    #Validation
    required_fields = {'userid', 'course_name', 'pdf_URL'}
    if not data or not all(field in data for field in required_fields):
        return jsonify({'Error':'Missing userid, course_name or pdf_URL'}),400
    #End
    
    userid = data['userid']
    course_name = data['course_name']
    pdf_URL = data['pdf_URL']

    try:
        response = (supabase.table('notes')
                    .delete()
                    .eq('userid',userid)
                    .eq('course_name',course_name)
                    .eq('pdf_URL',pdf_URL)
                    .execute())
        print(response.data)
        if response.data!=[]:
            return jsonify({"Message":'Note deleted successfully!'}),201
        else: 
            return jsonify({"Error": 'Note not found!'}),404
        
    except Exception as e:
        return jsonify({"Error":str(e)}),500

    

if __name__=='__main__':
    print("This is flask for " + os.path.basename(__file__) + ": notes ...")
    app.run(debug=True)
