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

# pre define varriables--------------------------------------------------------------------------------------
base_model_path = os.path.expanduser('C:/Users/ASUS/.cache/whisper/base.pt')# Voice Model paths
tiny_model_path = os.path.expanduser('C:/Users/ASUS/.cache/whisper/tiny.pt')# Voice Model Paths
model = whisper.load_model(base_model_path) # Currunt Using Voice Model

gptModel = GPT4All("E:\Projects\Assistant\AI Models\gpt4all-falcon-q4_0.gguf", allow_download=False)# GPT4all Modal Path

listener = sr.Recognizer()
mic = sr.Microphone()

engine = pyttsx3.init()
engine.setProperty('rate',145)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)# Get Male Voice

wake_word = "alex" # Give Name for Assistant
#------------------------------------------------------------------------------------------------------------

def elevanlabs(text):# elevanlabs text to speech
    naturalvoice = elevenlabs.Voice(voice_id="XB0fDUnXU5powFXDhCwa", settings=elevenlabs.VoiceSettings(stability=1,similarity_boost=0.95))
    audio = elevenlabs.generate(text=text,voice=naturalvoice)
    elevenlabs.play(audio)

def speak(text):# python text to speech
    engine.say(text)
    engine.runAndWait()

def start_listening():# get user command as sound
    try:
        with mic as source:
            listener.adjust_for_ambient_noise(source, duration=2)
            print("I'm listening Sir...")
            uservoice = listener.listen(mic) 
            return uservoice
    except:
        print("Mic error") # Test Only
        pass

def get_user_command_as_text(voice):# Convert User Voice To Text
    with open("userVoice.wav", "wb") as f:
        f.write(voice.get_wav_data())
    result = model.transcribe("userVoice.wav", language= 'en', fp16=False)
    print(result["text"])
    promptText = result["text"]
    promptText = promptText.lower()
    return promptText             
    
def render_in_gpt4all(text):# get gpt prompt
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

