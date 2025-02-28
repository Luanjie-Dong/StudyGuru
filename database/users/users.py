#!/usr/bin/env python3
from supabaseClient import supabase
from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)

CORS(app)

@app.route('/users', methods=['POST'])
def add_one_user():
    """
    Sample Data:
    {
        "firebase_uid":"c6dd5e2b-9c1d-4109-8ba3-3e246c9ec813"
    }

    Returns:
    {
        "Message:": "User c6dd5e2b-9c1d-4109-8ba3-3e246c9ec813 added!",
        "userid": "c6dd5e2b-9c1d-4109-8ba3-3e246c9ec813"
    }
    """
    data=request.get_json()
    required_fields={'firebase_uid'}
    if not data or not all(field in data for field in required_fields):
        return jsonify({'Error':'Missing firebase_uid.'}),400
    
    firebase_uid=data['firebase_uid']

    try:
        response=supabase.table('users').insert({"userid":firebase_uid}).execute()
        if response.data:
            return jsonify({"Message:":f"User {firebase_uid} added!",
                            "userid":response.data[0]['userid']}),201
        else:
            return jsonify({"Error": f'User not added...'}),500
        
    except Exception as e:
        return jsonify({"Error":str(e)}),500


@app.route("/users", methods=['GET'])
def get_one_user_info():
    """
        PARAMS:
        userid:c6dd5e2b-9c1d-4109-8ba3-3e246c9ec815
            
        Returns:
        [
            {
                "created_at": "2025-02-14T14:46:22.1489+00:00",
                "power_freeze": 0,
                "power_hint": 0,
                "power_option": 0,
                "userid": "c6dd5e2b-9c1d-4109-8ba3-3e246c9ec815",
                "username": "test2"
            }
        ]
    """
    
    userid = request.args.get('userid')
    if not userid:
        return jsonify({'Error':'Missing userid.'}),400
    try:
        response = (
            supabase.table('users')
            .select('*')
            .eq('userid',userid)
            .execute())
        if response.data:
            return jsonify(response.data),200
        else:
            return jsonify({'Error':"User not found"}),404
    except Exception as e:
        return jsonify({"Error":str(e)}),500
    

if __name__=='__main__':
    print("This is flask for " + os.path.basename(__file__) + ": users ...")
    app.run(host='0.0.0.0',debug=True, port=5000)

    