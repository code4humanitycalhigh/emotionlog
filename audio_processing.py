from google.cloud import speech
import text2emotion as te
import speech_recognition as sr
from time import sleep
import os
import keyboard
from datetime import datetime
import time
import pyaudio
import wave
import io

def record():

    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i)["name"])
    index=int(input("Choose index: "))


    go = 1

    def quit():
        
        print("exiting...")
        nonlocal go
        go = 0

    keyboard.on_press_key("q", lambda _:quit())
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 2
    fs = 44100  # Record at 44100 samples per second
    seconds = 100
    

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input_device_index=index,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)
        if go==0:
            break


    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    name = 'log_'+datetime.now().strftime("%m-%d_%H-%M")
    path = 'recordings/'+name+'.wav'

    wf = wave.open(path, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
    return path


def wav_to_text(file_name):
#setting Google credential
  os.environ['GOOGLE_APPLICATION_CREDENTIALS']= 'google_secret_key.json'
  # create client instance 
  client = speech.SpeechClient()
  #the path of your audio file
  
  with io.open(file_name, "rb") as audio_file:
      content = audio_file.read()
      audio = speech.RecognitionAudio(content=content)


  config = speech.RecognitionConfig(
      encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
      enable_automatic_punctuation=True,
      audio_channel_count=1,
      language_code="en-US",
  )

  # Sends the request to google to transcribe the audio
  response = client.recognize(request={"config": config, "audio": audio})
  text=''
  # Reads the response
  for result in response.results:
      text+=result.alternatives[0].transcript
  return text

def emotion_detection(text):
   return te.get_emotion(text)



#print(emotion_detection(wav_to_text("recordings/test2.wav")))
#print(record())

