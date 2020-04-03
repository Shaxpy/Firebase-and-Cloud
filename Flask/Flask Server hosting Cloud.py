#FIRESTORE Cloud data being sent through flask server to LocalHost! 
##Using Query 'GET'

import os

from firebase_admin import credentials, firestore, initialize_app

from flask import Flask, request, jsonify
app = Flask(__name__)

cred = credentials.Certificate('serviceAccountKey.json')

default_app = initialize_app(cred)

db = firestore.client()

database_ref = db.collection('entities')

@app.route('/', methods=['GET'])

def read():

    try:
        pm25 = request.args.get('pm25')
        dt = request.args.get('DateTime')
        if pm25 and dt:
            pm25_data = database_ref.document(pm25)
            dt_data = database_ref.document(dt)
            
            return jsonify({'DateTime': dt_data, 'PM2.5': pm25_data}), 200
        else:

            all_todos = [doc.to_dict() for doc in database_ref.stream()]

            return jsonify(all_todos), 200
    
    
    except Exception as e:

        return f"An Error Occured: {e}"

if __name__ == '__main__':

    app.run(port = 4010, debug = True)
