import time
import pyttsx3
import speech_recognition as sr
import eel
from langdetect import detect  # Install using pip install langdetect
import webbrowser
import re

# Initialize pyttsx3 engine globally to avoid re-initializing in every function
engine = pyttsx3.init()

def speak(text, language='en'):
    """Speak the given text in the specified language."""
    voices = engine.getProperty('voices')

    # Set voice based on language
    if language.startswith('en'):  # English
        engine.setProperty('voice', voices[1].id)  # Select English voice
    elif language.startswith('hi'):  # Hindi
        for voice in voices:
            if "hindi" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
    else:
        engine.setProperty('voice', voices[0].id)  # Default voice

    # Set speed and speak text
    engine.setProperty('rate', 170)
    eel.DisplayMessage(text)  # Display in UI
    engine.say(text)
    engine.runAndWait()

@eel.expose
def takeCommand():
    """Listen to the user's speech and recognize it."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            print('Listening...')
            eel.DisplayMessage('Listening...')
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=10, phrase_time_limit=6)

            print('Recognizing...')
            eel.DisplayMessage('Recognizing...')
            query = r.recognize_google(audio, language='hi-IN')  # Support for Hindi recognition
            print(f'User said: {query}')
            
            # Detect the language of the recognized query
            detected_language = detect(query)
            print(f"Detected language: {detected_language}")
            
            # Speak the input back to the user
            speak(f"आपने कहा: {query}" if detected_language == 'hi' else f"You said: {query}", language=detected_language)
            eel.DisplayMessage(query)  # Display text in UI
            
            return query.lower(), detected_language

        except sr.UnknownValueError:
            error_msg = "मुझे समझ नहीं आया।" if detected_language == 'hi' else "Sorry, I could not understand that."
            print(error_msg)
            speak(error_msg)
            return "", ""
        except sr.RequestError:
            error_msg = "स्पीच सेवा में समस्या है।" if detected_language == 'hi' else "There was an issue connecting to the speech recognition service."
            print(error_msg)
            speak(error_msg)
            return "", ""
        except Exception as e:
            print(f"Error: {e}")
            return "", ""

@eel.expose
def allCommands():
    """Process recognized commands and perform actions."""
    query, lang = takeCommand()
    if not query:
        return  # Stop execution if no input

    print(f"Processing Command: {query}")
    eel.DisplayMessage(f"Processing Command: {query}")

    if lang == 'hi':
        # Hindi Commands
        if 'यूट्यूब खोलो' in query:  # Open YouTube
            speak("यूट्यूब खोल रहा हूँ।", language='hi')
            webbrowser.open("https://www.youtube.com")

        elif 'यूट्यूब पर खोजो' in query:  # Search YouTube
            search_query = query.split('यूट्यूब पर खोजो')[-1].strip()
            if search_query:
                speak(f"यूट्यूब पर {search_query} खोज रहा हूँ।", language='hi')
                youtube_url = f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}"
                webbrowser.open(youtube_url)
            else:
                speak("कृपया खोज शब्द बताएं।", language='hi')

        elif 'समय बताओ' in query:  # Time Command
            current_time = time.strftime("%H:%M:%S")
            speak(f"वर्तमान समय है {current_time}", language='hi')

        elif 'बंद करो' in query:  # Exit Command
            speak("अलविदा!", language='hi')
            eel.closeApp()

        else:
            speak("मुझे आदेश समझ में नहीं आया।", language='hi')

    else:
        # English Commands
        if 'youtube' in query:
            if 'open' in query:
                speak("Opening YouTube", language='en')
                webbrowser.open("https://www.youtube.com")
            elif 'search' in query:
                search_query = re.sub(r'\bsearch\b', '', query).strip()
                if search_query:
                    speak(f"Searching YouTube for {search_query}", language='en')
                    youtube_url = f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}"
                    webbrowser.open(youtube_url)
                else:
                    speak("Please specify a search query for YouTube.", language='en')

        elif 'time' in query:
            current_time = time.strftime("%H:%M:%S")
            speak(f"The current time is {current_time}", language='en')

        elif 'exit' in query or 'quit' in query:
            speak("Goodbye!", language='en')
            eel.closeApp()

        else:
            speak("Sorry, I did not recognize the command.", language='en')

    eel.ShowHood()
