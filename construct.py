import speech_recognition as sr
import pyttsx3
import requests
import time

# Configuration
WAKE_WORD = "holocron"
SERVER_URL = "http://localhost:5001"

# Initialize TTS
engine = pyttsx3.init()
def speak(text):
    print(f"[Construct] Speaking: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("[Construct] Listening...")
        audio = r.listen(source)
    
    try:
        text = r.recognize_google(audio).lower()
        print(f"[Construct] Heard: {text}")
        return text
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        speak("Voice service unavailable.")
        return ""

def process_command(text):
    if "status" in text:
        # Fetch status from server
        # resp = requests.get(f"{SERVER_URL}/api/status")
        speak("Systems are operational. Gold reserves steady.")
    elif "market" in text:
        speak("Checking Goblin Stack. Draconic Runes are up 20 percent.")
    elif "where is" in text:
        item = text.split("where is")[-1].strip()
        speak(f"Searching for {item}. One moment.")
        # requests.get(...)
    else:
        speak("Command not recognized.")

if __name__ == "__main__":
    speak("Construct Online.")
    while True:
        text = listen()
        if WAKE_WORD in text:
            speak("Yes?")
            command = listen()
            if command:
                process_command(command)
