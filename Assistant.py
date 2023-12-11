import whisper
import os
import speech_recognition as sr
from gpt4all import GPT4All

base_model_path = os.path.expanduser('C:/Users/ASUS/.cache/whisper/base.pt')
tiny_model_path = os.path.expanduser('C:/Users/ASUS/.cache/whisper/tiny.pt')

gptModel = GPT4All("E:\Projects\Assistant\AI Models\gpt4all-falcon-q4_0.gguf", allow_download=False)

listener = sr.Recognizer()
model = whisper.load_model(tiny_model_path)

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


