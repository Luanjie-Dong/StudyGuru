#!/usr/bin/env python3
from supabaseClient import supabase
from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)

CORS(app)

@app.route("/module", methods=['GET'])
def get_all_modules():
    """
        PARAMS:
        course_id:502a0caa-8812-424f-9490-eb73f2722ac0
    
        Returns:
        [
            {
                "course_id": "d14c272a-e38d-4cfb-b952-e2617029a2d2",
                "module_id": "6daed838-26af-47dc-8354-6ba7a7a4810a",
                "module_name": "Week 1"
            }
        ]
    """
    
    course_id = request.args.get('course_id')
    if not course_id:
        return jsonify({'Error':'Missing course_id'}),400
    
    try:
        response = (
            supabase.table('module')
            .select('*')
            .eq('course_id',course_id)
            .execute())
        if response.data:
            return jsonify(response.data),200
        else:
            return jsonify({'Error':"Course has no modules!"}),404
    except Exception as e:
        return jsonify({"Error":str(e)}),500
    

@app.route("/module", methods=['POST'])
def add_one_module():
    data = request.get_json()
    '''
        Sample data:
        { 
            "module_name":"Week 1",
            "course_id":"d14c272a-e38d-4cfb-b952-e2617029a2d2"
        }
        Returns:
        {
            "Message": "Module added successfully!",
            "module_id": "a6efb5ac-c0aa-4b81-8541-cfea248f786a"
        }
    '''
    
    #Validation
    required_fields = {'module_name', 'course_id'}
    if not data or not all(field in data for field in required_fields):
        return jsonify({'Error':'Missing module_name or course_id!'}),400
    #End
    
    course_id = data['course_id']
    module_name = data['module_name']
    insert_data = {"module_name":module_name, "course_id":course_id} #MISSING EMBEDDINGS FOR NOW

    try:
        response = supabase.table('module').insert(insert_data).execute()
        print(response)
        if response.data is not None:
            return jsonify({"Message":'Module added successfully!',
                            "module_id":response.data[0]['module_id']}),201
        else: 
            return jsonify({"Error": 'Module not added...'}),500
        
    except Exception as e:
        return jsonify({"Error":str(e)}),500
    


if __name__=='__main__':
    print("This is flask for " + os.path.basename(__file__) + ": module ...")
    app.run(debug=True)
