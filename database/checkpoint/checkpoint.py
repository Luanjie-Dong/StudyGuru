#!/usr/bin/env python3
from supabaseClient import supabase
from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)

CORS(app)

@app.route("/course_checkpoint", methods=['GET'])
def get_all_checkpoints_for_course():
    """
        PARAMS:
        course_id:d14c272a-e38d-4cfb-b952-e2617029a2d2

        Returns:
        [
            {
                "checkpoint_date": "2025-03-13T00:00:00+00:00",
                "checkpoint_id": "719ed46d-8b2e-4d4f-a10b-eec5280a05c5",
                "checkpoint_name": "Quiz 1",
                "course_id": "d14c272a-e38d-4cfb-b952-e2617029a2d2"
            }
        ]
    """
    
    course_id = request.args.get('course_id')
    if not course_id:
        return jsonify({'Error':'Missing course_id'}),400
    
    try:
        response = (
            supabase.table('checkpoint')
            .select('*')
            .eq('course_id',course_id)
            .execute())
        if response.data:
            return jsonify(response.data),200
        else:
            return jsonify({'Error':"User has no checkpoints!"}),404
    except Exception as e:
        return jsonify({"Error":str(e)}),500
    
@app.route("/checkpoint_date", methods=['GET'])
def get_all_checkpoints_by_date():
    """
        PARAMS:
        date:2025-02-27

        Returns:
        [
            {
                "checkpoint_date": "2025-03-13T00:00:00+00:00",
                "checkpoint_id": "719ed46d-8b2e-4d4f-a10b-eec5280a05c5",
                "checkpoint_name": "Quiz 1",
                "course_id": "d14c272a-e38d-4cfb-b952-e2617029a2d2"
            }
        ]
    """
    
    date = request.args.get('date')
    if not date:
        return jsonify({'Error':'Missing date!'}),400
    start_date = f"{date}T00:00:00+00:00"
    end_date = f"{date}T23:59:59+00:00"
    
    try:
        response = (
            supabase.table('checkpoint')
            .select('*')
            .gte('checkpoint_date',start_date)
            .lte('checkpoint_date',end_date)
            .execute())
        print(response.data)
        if response.data:
            return jsonify(response.data),200
        else:
            return jsonify([]),200
    except Exception as e:
        return jsonify({"Error":str(e)}),500
    

@app.route("/checkpoint", methods=['POST'])
def add_one_checkpoint():
    data = request.get_json()
    '''
        Sample request body:
        { 
            "course_id":"d14c272a-e38d-4cfb-b952-e2617029a2d2",
            "checkpoint_name":"Quiz 1",
            "checkpoint_date":"2025-03-13"
        }
        Returns:
        {
            "Message": "Checkpoint added successfully!"
        }
    '''
    
    #Validation
    required_fields={'course_id','checkpoint_name','checkpoint_date'}
    if not data or not all(field in data for field in required_fields):
        return jsonify({'Error':'Missing course_id, checkpoint_name or checkpoint_date.'}),400
    #End
    
    course_id = data['course_id']
    checkpoint_name = data['checkpoint_name']
    checkpoint_date = data['checkpoint_date']
    insert_data = {"course_id":course_id, "checkpoint_name":checkpoint_name, "checkpoint_date":checkpoint_date}

    try:
        response = supabase.table('checkpoint').insert(insert_data).execute()
        print(response)
        if response.data is not None:
            return jsonify({"Message":'Checkpoint added successfully!'}),201
        else: 
            return jsonify({"Error": 'Checkpoint not added...'}),500
        
    except Exception as e:
        return jsonify({"Error":str(e)}),500
    

@app.route("/checkpoint", methods=['DELETE'])
def delete_one_test():
    '''
        PARAMS: 
        checkpoint_id:719ed46d-8b2e-4d4f-a10b-eec5280a05c5

        Returns:
        {
            "Message": "Checkpoint deleted successfully!"
        }
    '''

    checkpoint_id = request.args.get('checkpoint_id')
    if not checkpoint_id:
        return jsonify({'Error':'Missing checkpoint_id!'}),400

    try:
        response = (supabase.table('checkpoint')
                    .delete()
                    .eq('checkpoint_id',checkpoint_id)
                    .execute())
        print(response.data)
        if response.data!=[]:
            return jsonify({"Message":'Checkpoint deleted successfully!'}),201
        else: 
            return jsonify({"Error": 'Checkpoint not found!'}),404
        
    except Exception as e:
        return jsonify({"Error":str(e)}),500

    

if __name__=='__main__':
    print("This is flask for " + os.path.basename(__file__))
    app.run(host='0.0.0.0',debug=True, port=5000)
