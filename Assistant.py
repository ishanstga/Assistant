import whisper
import os
import speech_recognition as sr
from gpt4all import GPT4All
import pyttsx3


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

#Openai whisper voice recognition model paths
base_model_path = os.path.expanduser('C:/Users/ASUS/.cache/whisper/base.pt')
tiny_model_path = os.path.expanduser('C:/Users/ASUS/.cache/whisper/tiny.pt')
model = whisper.load_model(tiny_model_path) #load methord

#gpt4all falcon model path
gptModel = GPT4All("E:\Projects\Assistant\AI Models\gpt4all-falcon-q4_0.gguf", allow_download=False)

#varriable for recognize audio input
listener = sr.Recognizer()

#varriable for text to speech
engine = pyttsx3.init()
engine.setProperty('rate',145)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

#Text to speech function
def speek(audio):
    engine.say(audio)
    engine.runAndWait()

#get prompt using whisper in offline
def listen_for_wake_word(audio):
    with open("english.wav", "wb") as f:
        f.write(audio.get_wav_data())
        result = model.transcribe("english.wav", language= 'en', fp16=False)
        print(result["text"])
        promptText = result["text"]
    return promptText

def gptPrompt(text):
    output = gptModel.generate(text, max_tokens=100)
    print(output)
    speek(output)

    #elevenlabs voice cordings----------------------------------------------------------------------
    #voice = elevenlabs.Voice(voice_id="XB0fDUnXU5powFXDhCwa", settings=elevenlabs.VoiceSettings(stability=1,similarity_boost=0.75))
    #audio = elevenlabs.generate(text=output,voice=voice)
    #elevenlabs.play(audio)

try:
    with sr.Microphone() as source:
        listener.adjust_for_ambient_noise(source, duration=1)
        print("listening...")
        voice = listener.listen(source)
        prompt = listen_for_wake_word(voice)
        gptPrompt(prompt)
        
except:
    print("exept pass")
    pass
