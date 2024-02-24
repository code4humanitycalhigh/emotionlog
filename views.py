from flask import Flask, render_template, request, jsonify
from face_detector import track_emotions
from audio_processing import wav_to_text,emotion_detection,record
from flask_app import app

@app.route("/",methods=['GET','POST'])
def index():
    if request.method == "POST":
      #face_data=track_emotions('model2')
      #text_data=track_emotions(wav_to_text(file))
      print('t')
      record()
      data=track_emotions('model2')

      return render_template("index.html",data=data)
    return render_template("index.html")