import speech_recognition as sr
from gpt4all import GPT4All
import whisper
import os
import pyttsx3
from time import sleep
import elevenlabs

#test text to voice------------------------------------------------------------------------------------------
'''
from bark import SAMPLE_RATE, generate_audio, preload_models

# download and load all models
preload_models()

# generate audio from text
text_prompt = """
     Hello, my name is Suno. And, uh — and I like pizza. [laughs] 
     But I also have other interests such as playing tic tac toe.
"""
audio_array = generate_audio(text_prompt)
'''
#------------------------------------------------------------------------------------------------------------

base_model_path = os.path.expanduser('C:/Users/ASUS/.cache/whisper/base.pt')
tiny_model_path = os.path.expanduser('C:/Users/ASUS/.cache/whisper/tiny.pt')
model = whisper.load_model(base_model_path)

gptModel = GPT4All("E:\Projects\Assistant\AI Models\gpt4all-falcon-q4_0.gguf", allow_download=False)

listener = sr.Recognizer()
mic = sr.Microphone()

engine = pyttsx3.init()
engine.setProperty('rate',145)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

A = open("APIkey.txt", "r")
API = A.read()
elevenlabs.set_api_key(API)

wake_word = "alex"

def elevanlabs(text):
    naturalvoice = elevenlabs.Voice(voice_id="XB0fDUnXU5powFXDhCwa", settings=elevenlabs.VoiceSettings(stability=1,similarity_boost=0.95))
    audio = elevenlabs.generate(text=text,voice=naturalvoice)
    elevenlabs.play(audio)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def start_listening():
    try:
        with mic as source:
            listener.adjust_for_ambient_noise(source, duration=2)
            print("listening...")
            uservoice = listener.listen(mic) 
            return uservoice
    except:
        print("Mic error")
        pass

def get_user_command_as_text(voice):
    # Convert Voice To Text
    with open("english.wav", "wb") as f:
        f.write(voice.get_wav_data())
    result = model.transcribe("english.wav", language= 'en', fp16=False)
    print(result["text"])
    promptText = result["text"]
    promptText = promptText.lower()
    return promptText             
    
      

def render_in_gpt4all(text):
    output = gptModel.generate(text, max_tokens=200)
    print(output)
    return output

while True:
    userVoice = start_listening()
    promptText = get_user_command_as_text(userVoice)
    if wake_word in promptText:
        gptOutput = render_in_gpt4all(promptText)
        speak(gptOutput)
    else:
        print(wake_word + " is not in command")

