from flask import Flask, render_template, request, jsonify
from facial_detector import track_emotions
from flask_app import app

@app.route("/",methods=['GET','POST'])
def index():
    if request.method == "POST":
      print('t')
      return render_template("index.html",data=track_emotions('model2'))
    return render_template("index.html")