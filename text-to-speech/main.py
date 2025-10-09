import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init()

engine.say("Say something")
engine.runAndWait()

recognizer = sr.Recognizer()
try:
    with sr.Microphone() as source:
        print("Listening...")
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source, duration=1)
        # Listen for audio
        audio = recognizer.listen(source)
        
        print("Processing...")
        # Recognize speech using Google Speech Recognition
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        
except sr.UnknownValueError:
    print("Sorry, I could not understand the audio")
except sr.RequestError as e:
    print(f"Could not request results; {e}")
except Exception as e:
    print(f"An error occurred: {e}")