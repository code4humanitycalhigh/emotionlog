from google.cloud import speech
import text2emotion as te
from speech_recognition import AudioSource, AudioData
import speech_recognition as sr
from time import sleep
import os
import keyboard
from datetime import datetime
import time
import io
def test():
    go = 1

    def quit():
        
        print("exiting...")
        nonlocal go
        go = 0

    keyboard.on_press_key("q", lambda _:quit()) # press q to quit

    r = sr.Recognizer()
    mic = sr.Microphone()
    #print(sr.Microphone.list_microphone_names())

    mic = sr.Microphone(device_index=1)

    print('listening...')
    while go:
        try:
            sleep(0.01)
            with mic as source:
                audio = r.listen(source)
                #print('go: ',go)
                #print(r.recognize_google(audio))
        except Exception as e:
            print(e)
            pass
    
    name = 'log_'+datetime.now().strftime("%m-%d_%H-%M")
    path = 'recordings/'+name+'.wav'
    with open(path,"wb") as file:
        file.write(audio.get_wav_data())
    print('uploading to '+path)
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
#print(record_audio())
test()
