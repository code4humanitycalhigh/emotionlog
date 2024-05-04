from flask import Flask, render_template, request, jsonify
from audio_processing import wav_to_text,emotion_detection,record
from flask_app import app
import cv2
import json
import pyaudio
import threading 
import numpy as np
from keras.models import model_from_json
import classifier
import pandas as pd
from datetime import datetime


face_detector = cv2.CascadeClassifier("ml_folder/haarcascade_frontalface_default.xml")

global emotions
emotions={
    'angry':[0],
    'disgust':[0],
    'fear':[0],
    'happy':[0],
    'sad':[0],
    'surprise':[0],
    'neutral':[0]
}

global mic_list
mic_list=[]

# Load the Model and Weights
model = model_from_json(open("ml_folder/facial_expression_model_structure.json", "r").read())
model.load_weights('ml_folder/facial_expression_model_weights.h5')
model.make_predict_function()

video_df = pd.read_csv("data/video_recognition.csv")
audio_df = pd.read_csv("data/audio_recognition.csv")


# -----------FLASK PAGES
@app.route("/",methods=['GET','POST'])
def index():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')

    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            mic_list.append(p.get_device_info_by_host_api_device_index(0, i)["name"])
            #print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i)["name"])
    #index=int(input("Choose index: "))
    return render_template("index.html",mic_list=mic_list[1:])
    
@app.route("/log", methods=["GET","POST"])
def log():
   return render_template("log.html")

@app.route("/analytics", methods=["GET","POST"])
def analytics():
   return render_template("analytics.html")




# -----------FLASK AJAX METHODS
@app.route("/start_recording",methods=['GET','POST'])
def start_recording():
    if request.method=='POST':
    
        print('started')
        audio_emotions= emotion_detection(wav_to_text(record(1)))
        print(audio_emotions)

        #uploading to csv
        upload_to_csv("audio",audio_emotions)

        return 'done'



@app.route('/uploade', methods=['POST', 'GET'])
def upload_file():
    #print("upload_file")1
    if request.method == 'POST':
        #print("request=post/uploade")
        # f.save("somefile.jpeg")
        # f = request.files['file']

        f = request.files['file'].read()
        npimg = np.fromstring(f, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_GRAYSCALE)
        face_properties = classifier.classify(img, face_detector, model)
        if len(face_properties)>0:
            #print("server: ",face_properties)
            try:
                emotions[face_properties[0]['label']].append(int(face_properties[0]['score']))
            except Exception as e:
                print(e)
            #print(emotions)
        
        
        return json.dumps(face_properties)

@app.route('/done', methods=['POST', 'GET'])  
def done():
    if request.method=='POST':
        print("finished, uploading data to emotions")
        for key in emotions:
            #print(key)
            try:
                emotions[key]=round(sum(emotions[key])/len(emotions[key]),2)
            except Exception as e:
                print(e)
                #print(emotions[key])
                #print(emotions)
                print("\n")
        print(emotions)
        
        #uploading to csv file
        upload_to_csv("video",emotions)

        

        return 'done'

@app.route('/select_mic', methods=['GET','POST'])
def select_mic():
    print("select_mic reached")
    if request.method=='POST':
        print("select_mic post")
        mic=request.form['mic']
        print(mic)
    else:
        return render_template('index.html')


def upload_to_csv(type,data):
    if (type=="video"):
        df=video_df
        csv="video_recognition.csv"
    elif (type=="audio"):
        df=audio_df
        csv="audio_recognition.csv"
    
    today = datetime.today()
    formatted_date = today.strftime("%d/%m/%y")
    emotions_list=[formatted_date]
    for key in data:
        emotions_list.append(data[key])
    df.loc[len(df)] = emotions_list

    
    df.to_csv("data/"+csv, index=None)

