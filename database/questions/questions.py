#!/usr/bin/env python3
from supabaseClient import supabase
from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)

CORS(app)

@app.route("/questions", methods=['POST'])
def add_questions():
    data = request.get_json()
    '''
    BULK insert questions. If any of the insertion fails, none of the questions will be inserted.
    Format: List of JSON questions.

        Sample data:
            [{ 
                "challenge_id":"8c5ab830-1708-47c0-9a72-60ff07df6cef",
                "question_no":"1",
                "question_detail":{
                    "question": "What is 4+3",
                    "type": "multi-select",
                    "options": [1,2,3,7]
                    },
                "answer":["7"],
                "hint":"Addition"
            }]
        Returns:
        {
            "Message": "Question No 1 for challenge_id 8c5ab830-1708-47c0-9a72-60ff07df6cef added successfully!",
        }
    '''
    
    #Validation
    if not isinstance(data, list):
        return jsonify({'Error': 'Input must be a list of questions'}), 400
    
    required_fields={'challenge_id','question_no','question_detail','answer','hint'}
    required_question_fields={'question','type','options'}

    for question_data in data:
        if not isinstance(question_data,dict) or not all(field in question_data for field in required_fields):
            return jsonify({'Error':'Missing challenge_id, question_no, question_detail, answer, or hint.'}),400
        if not isinstance(question_data['question_detail'],dict) or not all(field in question_data['question_detail'] for field in required_question_fields):
            return jsonify({"Error:":f'Question object must contain {",".join(required_question_fields)}'}),400
    #End
    
    insert_data = data

    try:
        response = supabase.table('questions').insert(insert_data).execute()
        print(response)
        if response.data is not None:
            return jsonify({"Message":f'All {len(data)} questions added successfully!',}),201
        else: 
            return jsonify({"Error": 'Questions not added...'}),500
        
    except Exception as e:
        return jsonify({"Error":str(e)}),500


@app.route("/questions", methods=['GET'])
def get_all_questions_for_challenge():
    """
    Used for first time viewing of questions or during a replay. (Actual replaying, not view past attempts.)

        PARAMS:
        challenge_id:c5618f8d-06cb-43b9-8739-9bc325f2dfe5
        
        Returns:
        [
            {
                "answer": ["7"],
                "hint": "Addition",
                "question_detail":{
                    "question": "What is 4+3",
                    "type": "multi-select",
                    "options": [1,2,3,7],
                    },
                "question_no": 1
            }
        ]

    """

    challenge_id = request.args.get('challenge_id')
    if not challenge_id:
        return jsonify({'Error':'Missing challenge_id'}),400

    try:
        response = (
            supabase.table('questions')
            .select('question_no','question_detail','answer','hint')
            .eq('challenge_id',challenge_id)
            .execute())
        if response.data:
            return jsonify(response.data),200
        else:
            return jsonify({'Error':"User has no questions for this challenge!"}),404
    except Exception as e:
        return jsonify({"Error":str(e)}),500
    

@app.route("/questions_attempt", methods=['GET'])
def get_all_questions_for_challenge_recent_attempt():
    """
    Used to view most recent attempt of challenge.
    
    PARAMS:
    challenge_id:80a31e9d-bf30-4d5d-8bdd-f27d0c69c73e

    Returns:
        [
            {
                "answer": ["7"],
                "correct": null,
                "explanation": null,
                "input": null,
                "question_detail": {
                    "options": [1,2,3,7],
                    "question": "What is 4+3",
                    "type": "multi-select"
                },
                "question_no": 1,
                "question_score": 0
            }
        ]

    """
    challenge_id=request.args.get('challenge_id')
    if not challenge_id:
        return jsonify({'Error':'Missing challenge_id'}),400
    
    try:
        response = (
            supabase.table('questions')
            .select('question_no','question_detail','input','answer','explanation','correct','question_score')
            .eq('challenge_id',challenge_id)
            .execute())
        if response.data:
            return jsonify(response.data),200
        else:
            return jsonify({'Error':"User has no questions for this challenge!"}),404
    except Exception as e:
        return jsonify({"Error":str(e)}),500
    

@app.route("/questions", methods=['PUT'])
def update_one_question():
    data = request.get_json()
    '''
    Used for marking questions and updating them.

        Sample data:
        { 
            "question_id":"dab350e4-94b7-4930-884b-7f777bbe2c03",
            "input":"21",
            "explanation":"4+3 is 7 u kinda stupid",
            "correct":"False",
            "question_score":4
        }
        Returns:
        {
            "Message": "Question No 3 for challenge_id c5618f8d-06cb-43b9-8739-9bc325f2dfe5 updated successfully!"
        }
    '''
    
    #Validation
    required_fields={'question_id','input','explanation','correct','question_score'}
    if not data or not all(field in data for field in required_fields):
        return jsonify({'Error':'Missing question_id, input, explanation, correct or question_score.'}),400
    #End
    
    question_id = data["question_id"]
    input = data['input']
    explanation = data['explanation']
    correct = data['correct']
    question_score = data['question_score']
    update_data = {
        "input":input,
        "explanation":explanation,
        "correct":correct,
        "question_score":question_score,
        }

    try:
        response = (supabase.table('questions')
                    .update(update_data)
                    .eq('question_id',question_id)
                    .execute())
        print(response)
        if response.data!=[]:
            return jsonify({"Message":f'Question ID {question_id} updated successfully!',}),201
        else: 
            return jsonify({"Error": f'Question ID {question_id} not updated...'}),500
        
    except Exception as e:
        return jsonify({"Error":str(e)}),500
    



if __name__=='__main__':
    print("This is flask for " + os.path.basename(__file__) + ": questions ...")
    app.run(host='0.0.0.0',debug=True, port=5000)