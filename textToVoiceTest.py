import elevenlabs
text = "Yes, I am familiar with JavaScript. JavaScript is a programming language used to create dynamic and interactive web pages. It allows developers to add interactivity to their websites by manipulating the Document Object Model (DOM) of an HTML document."
voice = elevenlabs.Voice(voice_id="XB0fDUnXU5powFXDhCwa", settings=elevenlabs.VoiceSettings(stability=1,similarity_boost=0.95))
audio = elevenlabs.generate(text=text,voice=voice)
elevenlabs.play(audio)