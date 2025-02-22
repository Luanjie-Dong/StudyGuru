#!/usr/bin/env python3
from supabaseClient import supabase
from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)

CORS(app)

@app.route("/challenge", methods=['GET'])
def get_all_challenges_for_course():
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
                "challenge_id": "4e087bbd-765b-4802-b1f0-621f0c20b19f",
                "course_name": "ESD",
                "date": "2025-02-18T02:40:59+00:00",
                "challenge_score": 7,
                "type": "Daily"
            }
        ]
    """
    if not data or 'userid' not in data or 'course_name' not in data:
        return jsonify({'Error':'Missing userid or course_name'}),400
    
    userid = data['userid']
    course_name = data['course_name']
    try:
        response = (
            supabase.table('challenge')
            .select('course_name','challenge_id','type','challenge_score','date')
            .eq('userid',userid)
            .eq('course_name',course_name)
            .execute())
        if response.data:
            return jsonify(response.data),200
        else:
            return jsonify({'Error':"User has no challenges for this course!"}),404
    except Exception as e:
        return jsonify({"Error":str(e)}),500
    
@app.route("/challenge/<string:challenge_id>", methods=['GET'])
def get_one_challenge_score(challenge_id):
    '''
        Gets challenge score by retrieving and aggregating individual question scores from questions table.
        Updating of scores is done automatically, triggered by any update in score from related questions.
        
        NOT TRIGGERED BY INSERTION OF QUESTIONS.
        
        Place challenge_id in URL instead.
    '''
    try:
        response = (supabase.table('challenge')
                    .select('challenge_score')
                    .eq('challenge_id',challenge_id)
                    .execute())
        if response.data is not None:
            print(response.data)
            data = response.data
            return jsonify({"Message":'Challenge score retrieved!',
                            "Score":data[0]['challenge_score']}),201
        else: 
            return jsonify({"Error": 'Challenge has no questions.'}),500
        
    except Exception as e:
        return jsonify({"Error":str(e)}),500
    

if __name__=='__main__':
    print("This is flask for " + os.path.basename(__file__) + ": questions ...")
    app.run(debug=True)
    


@app.route("/challenge", methods=['POST'])
def add_one_challenge():
    data = request.get_json()
    '''
    Returns challenge_id for respective question adding.
        Sample data:
        { 
            "userid":"502a0caa-8812-424f-9490-eb73f2722ac0",
            "course_name":"ESM",
            "type":"Normal"
        }
        Returns:
        {
            "Message": "Challenge added successfully!",
            "challenge_id": "678f29a2-e7f2-42cb-b84d-bb9a12765e95"
        }
    '''
    
    #Validation
    required_fields={'userid','course_name','type'}
    if not data or not all(field in data for field in required_fields):
        return jsonify({'Error':'Missing userid, course_name or type'}),400
    #End
    
    userid = data['userid']
    course_name = data['course_name']
    type = data['type']
    insert_data = {"userid":userid, "course_name":course_name, "type":type}

    try:
        response = supabase.table('challenge').insert(insert_data).execute()
        print(response)
        if response.data is not None:
            return jsonify({"Message":'Challenge added successfully!',
                            "challenge_id":response.data[0]["challenge_id"]}),201
        else: 
            return jsonify({"Error": 'Challenge not added...'}),500
        
    except Exception as e:
        return jsonify({"Error":str(e)}),500

    
    

if __name__=='__main__':
    print("This is flask for " + os.path.basename(__file__) + ": challenge ...")
    app.run(debug=True)
