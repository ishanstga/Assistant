import elevenlabs

A = open("APIkey.txt", "r")
API = A.read()
elevenlabs.set_api_key(API)

text  = "sure sir...! turning off pc. good bye.... see you next time."

voice = elevenlabs.Voice(voice_id="XB0fDUnXU5powFXDhCwa", settings=elevenlabs.VoiceSettings(stability=1,similarity_boost=0.95))
audio = elevenlabs.generate(text=text,voice=voice)
elevenlabs.play(audio)