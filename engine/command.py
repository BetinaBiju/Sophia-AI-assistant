import time
import pyttsx3
import speech_recognition as sr
import eel
from langdetect import detect  # Install using pip install langdetect

def speak(text, language='en'):
    """Speak the given text in the specified language."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    # Select voice based on language
    if language.startswith('en'):  # English
        engine.setProperty('voice', voices[1].id)  # English voice
    elif language.startswith('hi'):  # Hindi
        for voice in voices:
            if "hindi" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
    elif language.startswith('es'):  # Spanish
        for voice in voices:
            if "spanish" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break

    engine.setProperty('rate', 170)
    eel.DisplayMessage(text)  # For display in the UI
    engine.say(text)
    engine.runAndWait()

@eel.expose
def takeCommand():
    """Listen to the user's speech and recognize it."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        eel.DisplayMessage('Listening...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=10, phrase_time_limit=6)
    
    try:
        print('Recognizing...')
        eel.DisplayMessage('Recognizing...')
        # Use Google's recognizer to process speech (language set dynamically)
        query = r.recognize_google(audio)
        print(f'User said: {query}')
        
        # Detect the language of the recognized query
        detected_language = detect(query)
        print(f"Detected language: {detected_language}")
        
        # Map language codes to a readable name for TTS
        language_map = {'en': 'English', 'hi': 'Hindi', 'es': 'Spanish'}
        language_name = language_map.get(detected_language, 'English')

        print(f"Speaking in {language_name}...")
        speak(f"You said: {query}", language=detected_language)

        eel.DisplayMessage(query)  # Display recognized text in UI
        
    except Exception as e:
        print(f"Error: {e}")
        return ""
    
    return query.lower()

@eel.expose
def allCommands():
    query = takeCommand()
    if not query:
        return  # If no input, stop execution

    print(query)

    if 'open' in query:
        from engine.features import openCommand
        openCommand(query)
    elif 'on youtube' in query:
        from engine.features import PlayYoutube
        PlayYoutube(query)
    else:
        print('Command not recognized')

    eel.ShowHood()

