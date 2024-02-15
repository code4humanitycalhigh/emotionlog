from google.cloud import speech
import text2emotion as te
import os
import io

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



print(emotion_detection(wav_to_text("test2.wav")))