#!/usr/bin/env python3
from supabaseClient import supabase
from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)

CORS(app)

@app.route("/course", methods=['GET'])
def get_all_courses():
    data = request.get_json()
    """
        Sample data:
        {
            "userid":"502a0caa-8812-424f-9490-eb73f2722ac0"
        }
        Returns:
        {
            "course_id": "d14c272a-e38d-4cfb-b952-e2617029a2d2",
            "course_name": "DBTT",
            "created_at": "2025-02-22T06:57:01.417418+00:00",
            "streak": 0,
            "userid": "502a0caa-8812-424f-9490-eb73f2722ac0"
        }
    """
    if not data or 'userid' not in data:
        return jsonify({'Error':'Missing userid'}),400
    
    userid = data['userid']
    try:
        response = (
            supabase.table('course')
            .select('*')
            .eq('userid',userid)
            .execute())
        if response.data:
            return jsonify(response.data),200
        else:
            return jsonify({'Error':"User has no courses!"}),404
    except Exception as e:
        return jsonify({"Error":str(e)}),500
    

@app.route("/course", methods=['POST'])
def add_one_course():
    data = request.get_json()
    '''
        Sample data:
        { 
            "userid":"502a0caa-8812-424f-9490-eb73f2722ac0",
            "course_name":"ESM"
        }
        Returns:
        {
            "Message": "Course added successfully!"
        }
    '''
    
    #Validation
    if not data or 'userid' not in data or 'course_name' not in data:
        return jsonify({'Error':'Missing userid or course_name'}),400
    #End
    
    userid = data['userid']
    course_name = data['course_name']
    insert_data = {"userid":userid, "course_name":course_name}

    try:
        response = supabase.table('course').insert(insert_data).execute()
        print(response)
        if response.data is not None:
            return jsonify({"Message":'Course added successfully!'}),201
        else: 
            return jsonify({"Error": 'Course not added...'}),500
        
    except Exception as e:
        return jsonify({"Error":str(e)}),500
    
@app.route("/course", methods=['DELETE'])
def delete_one_course():
    data = request.get_json()
    '''
        Sample data:
        { 
            "course_id":"d14c272a-e38d-4cfb-b952-e2617029a2d2"
        }
        Returns:
        {
            "Message": "Course deleted successfully!"
        }
    '''
    
    #Validation
    if not data or 'course_id' not in data:
        return jsonify({'Error':'Missing course_id'}),400
    #End
    
    course_id = data['course_id']

    try:
        response = (supabase.table('course')
                    .delete()
                    .eq('course_id',course_id)
                    .execute())
        print(response.data)
        if response.data!=[]:
            return jsonify({"Message":'Course deleted successfully!'}),201
        else: 
            return jsonify({"Error": 'Course not found!'}),404
        
    except Exception as e:
        return jsonify({"Error":str(e)}),500

@app.route("/course", methods=['PUT'])
def update_streak():
    data = request.get_json()
    """
    Sample Data:
    {
        "course_id":"d14c272a-e38d-4cfb-b952-e2617029a2d2",
        "completed_challenge":true
    }

    Returns:

    """
    #Validation
    required_fields={'course_id','completed_challenge'}
    if not data or not all(field in data for field in required_fields):
        return jsonify({'Error':'Missing course_id or completed_challenge'}),400
    #End
    
    course_id = data['course_id']
    completed_challenge = data['completed_challenge']
    try:
        response=(
            supabase.table('course')
            .select('streak')
            .eq('course_id',course_id)
            .execute()
        )
        if response.data:
            current_streak = response.data[0]['streak']
        else:
            return jsonify({"Error": f'Could not retrieve streak for course {course_id}...'}),500
        
        new_streak = current_streak +1 if completed_challenge else 0
        update_data = {
            'streak':new_streak
        }
        update_response=(supabase.table('course')
                        .update(update_data)
                        .eq('course_id',course_id)
                        .execute())
        
        if update_response.data:
            return jsonify({"Message":f'Streak for course {course_id} updated successfully!',}),201
        else: 
            return jsonify({"Error": f'Streak for course {course_id} not updated...'}),500

    except Exception as e:
         return jsonify({"Error":str(e)}),500


if __name__=='__main__':
    print("This is flask for " + os.path.basename(__file__) + ": courses ...")
    app.run(debug=True)
