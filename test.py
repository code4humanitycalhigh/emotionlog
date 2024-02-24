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

go = 1

def quit():
    
    print("exiting...")
    global go
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
            print('go: ',go)
            #print(r.recognize_google(audio))
    except Exception as e:
        print(e)
        pass
print('done')
name = 'log_'+datetime.now().strftime("%m-%d_%H-%M")
path = 'recordings/'+name+'.wav'
with open(path,"wb") as file:
    file.write(audio.get_wav_data())
print('uploading to '+path)