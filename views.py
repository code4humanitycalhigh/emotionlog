from flask import Flask, render_template, request, jsonify
#from face_detector import track_emotions
from audio_processing import wav_to_text,emotion_detection,record
from flask_app import app
import cv2
import json
import pyaudio
import threading 
import numpy as np
from keras.models import model_from_json
import classifier

face_detector = cv2.CascadeClassifier("ml/haarcascade_frontalface_default.xml")

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
model = model_from_json(open("ml/facial_expression_model_structure.json", "r").read())
model.load_weights('ml/facial_expression_model_weights.h5')
model.make_predict_function()




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
    return render_template("index.html",mic_list=mic_list)
    
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
        record(1)
        return 'done'

@app.route('/uploade', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        # f.save("somefile.jpeg")
        # f = request.files['file']

        f = request.files['file'].read()
        npimg = np.fromstring(f, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_GRAYSCALE)
        face_properties = classifier.classify(img, face_detector, model)
        #print(json.dumps(face_properties))
        #print(face_properties)
        try:
            emotions[face_properties[0]['label']].append(int(face_properties[0]['score']))
        except:
            pass
        return json.dumps(face_properties)

@app.route('/done', methods=['POST', 'GET'])  
def done():
    if request.method=='POST':
        for key in emotions:
            
            emotions[key]=round(sum(emotions[key])/len(emotions[key]),2)
        print(emotions)
        return 'done'

  

