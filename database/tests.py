#!/usr/bin/env python3
from supabaseClient import supabase
from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)

CORS(app)

@app.route("/tests", methods=['GET'])
def get_all_tests():
    data = request.get_json()
    """
        Sample data:
        {
            "userid":"502a0caa-8812-424f-9490-eb73f2722ac0"
        }
        Returns:
        [
            {
                "course_name": "ESD",
                "test_date": "2025-02-20T01:57:18+00:00",
                "test_name": "Mid terms"
            }
        ]
    """
    if not data or 'userid' not in data:
        return jsonify({'Error':'Missing userid'}),400
    
    userid = data['userid']
    try:
        response = (
            supabase.table('tests')
            .select('course_name','test_name','test_date')
            .eq('userid',userid)
            .execute())
        if response.data:
            return jsonify(response.data),200
        else:
            return jsonify({'Error':"User has no tests!"}),404
    except Exception as e:
        return jsonify({"Error":str(e)}),500
    

@app.route("/tests", methods=['GET'])
def get_all_tests_for_course():
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
                "course_name": "ESD",
                "test_date": "2025-02-20T01:57:18+00:00",
                "test_name": "Mid terms"
            }
        ]
    """
    if not data or 'userid' not in data or 'course_name' not in data:
        return jsonify({'Error':'Missing userid or course_name'}),400
    
    userid = data['userid']
    course_name = data['course_name']
    try:
        response = (
            supabase.table('tests')
            .select('course_name','test_name','test_date')
            .eq('userid',userid)
            .eq('course_name',course_name)
            .execute())
        if response.data:
            return jsonify(response.data),200
        else:
            return jsonify({'Error':"User has no tests for this course!"}),404
    except Exception as e:
        return jsonify({"Error":str(e)}),500
    

@app.route("/tests", methods=['POST'])
def add_one_test():
    data = request.get_json()
    '''
        Sample data:
        { 
            "userid":"502a0caa-8812-424f-9490-eb73f2722ac0",
            "course_name":"ESM",
            "test_name":"Quiz 1",
            "test_date":"2025-03-13"
        }
        Returns:
        {
            "Message": "Test added successfully!"
        }
    '''
    
    #Validation
    required_fields={'userid','course_name','test_name','test_date'}
    if not data or not all(field in data for field in required_fields):
        return jsonify({'Error':'Missing userid, course_name, test_name or test_date.'}),400
    #End
    
    userid = data['userid']
    course_name = data['course_name']
    test_name = data['test_name']
    test_date = data['test_date']
    insert_data = {"userid":userid, "course_name":course_name, "test_name":test_name, "test_date":test_date}

    try:
        response = supabase.table('tests').insert(insert_data).execute()
        print(response)
        if response.data is not None:
            return jsonify({"Message":'Test added successfully!'}),201
        else: 
            return jsonify({"Error": 'Test not added...'}),500
        
    except Exception as e:
        return jsonify({"Error":str(e)}),500
    

@app.route("/tests", methods=['DELETE'])
def delete_one_test():
    data = request.get_json()
    '''
        Sample data:
        { 
            "userid":"502a0caa-8812-424f-9490-eb73f2722ac0",
            "course_name":"ESM",
            "test_name":"Quiz 1"
        }
        Returns:
        {
            "Message": "Test deleted successfully!"
        }
    '''
    
    #Validation
    required_fields = {'userid','course_name','test_name'}
    if not data or not all(field in data for field in required_fields):
        return jsonify({'Error':'Missing userid, course_name or test_name'}),400
    #End
    
    userid = data['userid']
    course_name = data['course_name']
    test_name = data['test_name']

    try:
        response = (supabase.table('tests')
                    .delete()
                    .eq('userid',userid)
                    .eq('course_name',course_name)
                    .eq('test_name',test_name)
                    .execute())
        print(response.data)
        if response.data!=[]:
            return jsonify({"Message":'Test deleted successfully!'}),201
        else: 
            return jsonify({"Error": 'Test not found!'}),404
        
    except Exception as e:
        return jsonify({"Error":str(e)}),500

    

if __name__=='__main__':
    print("This is flask for " + os.path.basename(__file__) + ": tests ...")
    app.run(debug=True)
