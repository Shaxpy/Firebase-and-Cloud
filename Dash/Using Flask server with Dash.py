#This is an attempt to show graph of data recovered from FIRESTORE with FLask server using the GET query API
import dash
import dash_core_components as dcc
import plotly.graph_objs as go
import dash_html_components as html
import pandas as pd
import numpy as np
import os
import datetime
from firebase_admin import credentials, firestore, initialize_app

from flask import Flask, request, jsonify
server = Flask(__name__)
cred = credentials.Certificate('serviceAccountKey.json')
default_app = initialize_app(cred)
db = firestore.client()
database_ref = db.collection('entities')
x=[]
y=[]

@server.route('/', methods=['GET'])

def read():
    try:
        pm25 = request.args.get('pm25')
        dt = request.args.get('DateTime')
        if pm25 and dt:
            y = database_ref.document(pm25)
            x = database_ref.document(dt)
            
            return jsonify({'DateTime': x, 'PM2.5': y }), 200
    
    except Exception as e:
        return f"An Error Occured: {e}"

app = dash.Dash(__name__, server=server)

app.layout=html.Div([
    
    dcc.Graph(
    id='scatter_chart',
    figure={
        'data':[
            go.Scatter(
            x=x,
            y=y,
            mode='markers'
            )
        ],
        'layout':go.Layout(
        title='Scatterplot of Time',
        xaxis={'title':'DateTime'},
        yaxis={'title':'PM_25'})
    })
])

if __name__ == '__main__':

    server.run(port = 2149, debug = False)
