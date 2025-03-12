#!/usr/bin/env python3
from supabaseClient import supabase
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import datetime

app = Flask(__name__)

CORS(app)

def format_datetime(data):
    """Format datetime fields to be compatible with Java's LocalDateTime parser"""
    if isinstance(data, list):
        for item in data:
            if 'created_at' in item and item['created_at']:
                # Truncate microseconds to 3 digits (milliseconds) and remove timezone
                dt = datetime.datetime.fromisoformat(item['created_at'].replace('Z', '+00:00'))
                item['created_at'] = dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
    return data

@app.route("/course", methods=['GET'])
def get_all_courses():
    """
        PARAMS:
        userid:502a0caa-8812-424f-9490-eb73f2722ac0 (optional)
    
        Returns:
        {
            "course_id": "d14c272a-e38d-4cfb-b952-e2617029a2d2",
            "course_name": "DBTT",
            "created_at": "2025-02-22T06:57:01.417",  # Format compatible with Java LocalDateTime
            "streak": 0,
            "userid": "502a0caa-8812-424f-9490-eb73f2722ac0",
            "completed_challenge": false
        }
    """

    userid = request.args.get('userid')
    
    try:
        # If userid is provided, filter courses by that user
        if userid:
            response = (
                supabase.table('course')
                .select('*')
                .eq('userid', userid)
                .execute())
            if response.data:
                formatted_data = format_datetime(response.data)
                return jsonify(formatted_data), 200
            else:
                return jsonify([]), 200
        # If no userid is provided, return all courses
        else:
            response = (
                supabase.table('course')
                .select('*')
                .execute())
            if response.data:
                formatted_data = format_datetime(response.data)
                return jsonify(formatted_data), 200
            else:
                return jsonify([]), 200
    except Exception as e:
        return jsonify({"Error": str(e)}), 500

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
    '''
        PARAMS:
        course_id:d14c272a-e38d-4cfb-b952-e2617029a2d2

        Returns:
        {
            "Message": "Course deleted successfully!"
        }
    '''

    course_id = request.args.get('course_id')
    if not course_id:
        return jsonify({'Error':'Missing course_id'}),400
    
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
    ONLY CALL THIS IF USER HAS COMPLETED DAILY CHALLENGE FOR COURSE.

        Sample Data:
        {
            "course_id":"d14c272a-e38d-4cfb-b952-e2617029a2d2",
        }

        Returns:
        {
            "Message": "Streak for course d14c272a-e38d-4cfb-b952-e2617029a2d2 updated successfully!"
        }
    """
    #Validation
    required_fields={'course_id'}
    if not data or not all(field in data for field in required_fields):
        return jsonify({'Error':'Missing course_id'}),400
    #End
    
    course_id = data['course_id']

    try:
        response=(
            supabase.table('course')
            .select('streak','completed_challenge')
            .eq('course_id',course_id)
            .execute()
        )
        if response.data:
            current_streak = response.data[0]['streak']
            completed = response.data[0]['completed_challenge']
        else:
            return jsonify({"Error": f'Could not retrieve streak for course {course_id}...'}),500
        
        if completed:
            return jsonify({"Message:":f"Challenge for course {course_id} has already been completed!"}),201
        
        new_streak = current_streak +1
        update_data = {
            'streak':new_streak,
            'completed_challenge':True
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
    app.run(host='0.0.0.0',debug=True, port=5000)
