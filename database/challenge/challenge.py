#!/usr/bin/env python3
import os
from supabaseClient import supabase
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

@app.route("/challenge", methods=['GET'])
def get_all_challenges_for_course():
    """
        PARAMS:
        course_id:d14c272a-e38d-4cfb-b952-e2617029a2d2

        Returns:
        [
            {
                "challenge_id": "8c5ab830-1708-47c0-9a72-60ff07df6cef",
                "challenge_score": 0,
                "course_id": "d14c272a-e38d-4cfb-b952-e2617029a2d2",
                "date": "2025-02-22T08:50:45.155366+00:00",
                "type": "Normal"
            }
        ]
    """

    course_id=request.args.get('course_id')
    if not course_id:
        return jsonify({'Error':'Missing course_id!'}),400

    try:
        response = (
            supabase.table('challenge')
            .select('*')
            .eq('course_id',course_id)
            .execute())
        if response.data:
            return jsonify(response.data),200
        else:
            return jsonify({'Error':"User has no challenges for this course!"}),404
    except Exception as e:
        return jsonify({"Error":str(e)}),500
    
@app.route("/challengescore", methods=['GET'])
def get_one_challenge_score():
    '''
        Gets challenge score by retrieving and aggregating individual question scores from questions table.
        Updating of scores is done automatically, triggered by any update in score from related questions.
        
        NOT TRIGGERED BY INSERTION OF QUESTIONS.
        
        PARAMS:
        challenge_id:8c5ab830-1708-47c0-9a72-60ff07df6cef

        RETURNS:
        {
            "Message": "Challenge score retrieved!",
            "Score": 7
        }
    '''
    challenge_id=request.args.get('challenge_id')
    if not challenge_id:
        return jsonify({'Error':'Missing challenge_id!'}),400
    
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
    


@app.route("/challenge", methods=['POST'])
def add_one_challenge():
    data = request.get_json()
    '''
        Sample request body:
        { 
            "course_id":"d14c272a-e38d-4cfb-b952-e2617029a2d2",
            "type":"Normal"
        }
        Returns:
        {
            "Message": "Challenge added successfully!",
            "challenge_id": "8c5ab830-1708-47c0-9a72-60ff07df6cef"
        }
    '''
    
    #Validation
    required_fields={'course_id','type'}
    if not data or not all(field in data for field in required_fields):
        return jsonify({'Error':'Missing course_id or type!'}),400
    #End
    
    course_id = data['course_id']
    type = data['type']
    insert_data = {"course_id":course_id, "type":type}

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
    
@app.route("/challenge", methods=['PUT'])
def update_endtime():
    data = request.get_json()
    '''
        Sample request body:
        { 
            "challenge_id":"8c5ab830-1708-47c0-9a72-60ff07df6cef"
        }
        Returns:

    '''
    
    #Validation
    required_fields={"challenge_id"}
    if not data or not all(field in data for field in required_fields):
        return jsonify({'Error':'Missing challenge_id!'}),400
    #End
    
    challenge_id = data['challenge_id']
    update_data = {
        "end_datetime":"now()"
        }

    try:
        response = (supabase.table('challenge')
                    .update(update_data)
                    .eq('challenge_id',challenge_id)
                    .execute())
        print(response)
        if response.data is not None:
            return jsonify({"Message":f'Challenge ID {challenge_id} endtime updated successfully!',}),201
        else: 
            return jsonify({"Error": f'Challenge ID {challenge_id} endtime not updated...'}),500
        
    except Exception as e:
        return jsonify({"Error":str(e)}),500
    

if __name__=='__main__':
    print("This is flask for " + os.path.basename(__file__))
    app.run(host='0.0.0.0',debug=True, port=5000)
