#!/usr/bin/env python3
from supabaseClient import supabase
from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)

CORS(app)

@app.route("/friends", methods=['GET'])
def get_all_friends():
    '''
        PARAMS:
        userid:502a0caa-8812-424f-9490-eb73f2722ac0

        Returns:
        [
            {
                "friend_id": "c6dd5e2b-9c1d-4109-8ba3-3e246c9ec815"
            }
        ]
    '''
    
    userid = request.args.get('userid')
    if not userid:
        return jsonify({'Error':'Missing userid'}),400
    
    try:
        response = (
            supabase.table('friends')
            .select('friend_id')
            .eq('userid',userid)
            .execute())
        if response.data:
            return jsonify(response.data),200
        else:
            return jsonify({'Error':"User has no friends..."}),404
    except Exception as e:
        return jsonify({"Error":str(e)}),500
    

@app.route("/friends", methods=['POST'])
def add_one_friend():
    data = request.get_json()
    '''
        Sample data:
        { 
            "userid":"502a0caa-8812-424f-9490-eb73f2722ac0",
            "friend_id":"c6dd5e2b-9c1d-4109-8ba3-3e246c9ec815"
        }
        Returns:
        {
            "Message": "Friend added successfully!"
        }
    '''
    
    #Validation
    if not data or 'userid' not in data or 'friend_id' not in data:
        return jsonify({'Error':'Missing userid or friend_id'}),400
    #End
    
    userid = data['userid']
    friend_id = data['friend_id']
    insert_data = {"userid":userid, "friend_id":friend_id}

    try:
        response = supabase.table('friends').insert(insert_data).execute()
        if response.data is not None:
            return jsonify({"Message":'Friend added successfully!'}),201
        else: 
            return jsonify({"Error": 'Friend not added...'}),500
        
    except Exception as e:
        return jsonify({"Error":str(e)}),500

    

if __name__=='__main__':
    print("This is flask for " + os.path.basename(__file__) + ": friends ...")
    app.run(debug=True)
