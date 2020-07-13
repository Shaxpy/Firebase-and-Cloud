# Script to take real timee data from Weather API and use a model's pickle file to predict labels!

# from flask import Flask, jsonify, request
# import requests
# import json
# import pickle
# import pandas as pd

# model = pickle.load(open("prophet.pkl","rb"))

# def getData():
#     url = "https://api.climacell.co/v3/weather/realtime?lat=28.7041&lon=77.1025&location_id=delhi&unit_system=si&fields=wind_speed,wind_direction&apikey=Mrw0Md4UfRJva8xE2fsHWRrx1Hwfx6p9"
#     response = requests.get(url)
#     if response:
#         response = response.text
#         json_object = json.loads(response)
#         return json_object

# # print(response.text)
# def predictor():

#     wind_speed = []
#     wind_direction = []
#     date = ['2019-01-01 00:50:00']
#     weatherData = getData()
#     # date = weatherData['observation_time']['value']
#     wind_speed = weatherData['wind_speed']['value']
#     wind_direction = weatherData['wind_direction']['value']
#     myDict = {
#     	'ds' : date,
#         'Wind Speed (m/s)' : wind_speed,
#         'Wind Direction (°)' : wind_direction
#     }
#     inpt_df = pd.DataFrame.from_dict(myDict)
#     prediction = model.predict(inpt_df)
#     return prediction

# x = predictor()
# print(x['yhat'])

# data = getData()
# data

# data['wind_speed']['value']

# data['wind_direction']['value']

from flask import Flask, jsonify, request
import requests
import json
import pickle
import pandas as pd
from datetime import timedelta
from datetime import datetime

model = pickle.load(open("prophet.pkl","rb"))
ds = []
w_s = []
w_d = []
prediction = pd.DataFrame()
def getData():
    now = datetime.now() + timedelta(minutes=330)
    startTime = now.strftime("%Y-%m-%dT%H:%M:%SZ") 
    end = now + timedelta(hours=71)
    endTime = end.strftime("%Y-%m-%dT%H:%M:%SZ")
    customUrl = '&start_time='+startTime+'&end_time='+endTime
    url = "https://api.climacell.co/v3/weather/forecast/hourly?lat=28.7041&lon=77.1025&location_id=delhi&unit_system=si&fields=wind_speed%2Cwind_direction&apikey=57vLhf18DrPnHMFjuLDvywg7gCUGOwq5"
    response = requests.get(url+customUrl)
    if response:
        response = response.text
        json_object = json.loads(response)
        return json_object

# print(response.text)
def predictor():
    weatherData = getData()
    for i in range(0, len(weatherData)):
        wind_speed = []
        wind_direction = []
        date = []
        # startTime = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        # date = datetime.datetime.now() + datetime.timedelta(days=i)
        date = weatherData[i]['observation_time']['value'][0:10]
        # date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
        wind_speed = weatherData[i]['wind_speed']['value']
        wind_direction = weatherData[i]['wind_direction']['value']
        # myDict = {
            # 'index' : i,
        	# 'ds' : date,
            # 'Wind Speed (m/s)' : wind_speed,
            # 'Wind Direction (°)' : wind_direction
        # }
        # inpt_df = pd.DataFrame.from_dict(myDict)
        # prediction = model.predict(inpt_df)
        # pred = pd.DataFrame()
        # pred[i] = prediction
        
        ds.append(date)
        w_s.append(wind_speed)
        w_d.append(wind_direction)
    return ds,w_s,w_d

pred_ds,pred_ws,pred_wd = predictor()

# pred_ds = pred_ds.strftime("%Y-%m-%dT%H:%M:%SZ")

prediction['ds'] = pred_ds
# prediction['ds'] = prediction['ds'].replace(tzinfo=None)
# prediction['ds'].strftime('%Y-%m-%d %H:%M:%S')
prediction['Wind Speed (m/s)'] = pred_ws
prediction['Wind Direction (°)'] = pred_wd
# prediction.set_index('ds')

p = model.predict(prediction)
p

p['yhat']

new_df = pd.DataFrame()
new_df['ds'] = prediction['ds']
new_df['yhat'] = p['yhat']
new_df

new_df.to_csv('new_data.csv')





