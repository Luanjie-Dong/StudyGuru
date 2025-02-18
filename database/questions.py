#!/usr/bin/env python3
from supabaseClient import supabase
from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)

CORS(app)

@app.route("/questions", methods=['POST'])
def add_one_question():
    data = request.get_json()
    '''
        Sample data:
            { 
                "challenge_id":"c5618f8d-06cb-43b9-8739-9bc325f2dfe5",
                "question_no":"3",
                "question":{
                    "question": "What is 4+3",
                    "type": "multi-select",
                    "options": []
                    },
                "answer":"7",
                "hint":"Addition"
            }
        Returns:
        {
            "Message": "Question No 3 for challenge_id c5618f8d-06cb-43b9-8739-9bc325f2dfe5 added successfully!",
        }
    '''
    
    #Validation
    required_fields={'challenge_id','question_no','question','answer','hint'}
    if not data or not all(field in data for field in required_fields):
        return jsonify({'Error':'Missing challenge_id, question_no, question, answer, or hint.'}),400
    #End
    
    challenge_id = data['challenge_id']
    question_no = data['question_no']
    question = data['question']
    answer = data['answer']
    hint = data['hint']
    insert_data = {
        "challenge_id":challenge_id,
        "question_no":question_no,
        "question":question,
        "answer":answer,
        "hint":hint}

    try:
        response = supabase.table('questions').insert(insert_data).execute()
        print(response)
        if response.data is not None:
            return jsonify({"Message":f'Question No {question_no} for challenge_id {challenge_id} added successfully!',}),201
        else: 
            return jsonify({"Error": f'Question No {question_no} not added...'}),500
        
    except Exception as e:
        return jsonify({"Error":str(e)}),500


@app.route("/questions", methods=['GET'])
def get_all_questions_for_challenge():
    data = request.get_json()
    """
    Used for first time viewing of questions or during a replay. (Actual replaying, not view past attempts.)

        Sample data:
        {
            "challenge_id":"c5618f8d-06cb-43b9-8739-9bc325f2dfe5"
        }
        Returns:
        [
            {
                "answer": "7",
                "hint": "Addition",
                "question":{
                    "question": "What is 4+3",
                    "type": "multi-select",
                    "options": [],
                    },
                "question_no": 3
            }
        ]

    """
    if not data or 'challenge_id' not in data:
        return jsonify({'Error':'Missing challenge_id'}),400
    
    challenge_id = data['challenge_id']
    
    try:
        response = (
            supabase.table('questions')
            .select('question_no','question','answer','hint')
            .eq('challenge_id',challenge_id)
            .execute())
        if response.data:
            return jsonify(response.data),200
        else:
            return jsonify({'Error':"User has no questions for this challenge!"}),404
    except Exception as e:
        return jsonify({"Error":str(e)}),500
    

@app.route("/questions/<string:challenge_id>", methods=['GET'])
def get_all_questions_for_challenge_recent_attempt(challenge_id):
    """
    Used to view most recent attempt of challenge.

    Place challenge_id in URL instead.

    Returns:
    [
        {
            "answer": null,
            "correct": null,
            "explanation": null,
            "input": null,
            "question": null,
            "question_no": 1,
            "question_score": 3
        }
    ]

    """
    
    try:
        response = (
            supabase.table('questions')
            .select('question_no','question','input','answer','explanation','correct','question_score')
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
            "challenge_id":"c5618f8d-06cb-43b9-8739-9bc325f2dfe5",
            "question_no":"3",
            "input":"21",
            "explanation":"4+3 is 7 u kinda stupid",
            "correct":"False",
            "question_score":0
        }
        Returns:
        {
            "Message": "Question No 3 for challenge_id c5618f8d-06cb-43b9-8739-9bc325f2dfe5 updated successfully!"
        }
    '''
    
    #Validation
    required_fields={'challenge_id','question_no','input','explanation','correct','question_score'}
    if not data or not all(field in data for field in required_fields):
        return jsonify({'Error':'Missing challenge_id, question_no, input, explanation, correct or question_score.'}),400
    #End
    
    challenge_id = data['challenge_id']
    question_no = data['question_no']
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
                    .eq('challenge_id',challenge_id)
                    .eq('question_no',question_no)
                    .execute())
        print(response)
        if response.data is not None:
            return jsonify({"Message":f'Question No {question_no} for challenge_id {challenge_id} updated successfully!',}),201
        else: 
            return jsonify({"Error": f'Question No {question_no} not updated...'}),500
        
    except Exception as e:
        return jsonify({"Error":str(e)}),500
    



if __name__=='__main__':
    print("This is flask for " + os.path.basename(__file__) + ": questions ...")
    app.run(debug=True)