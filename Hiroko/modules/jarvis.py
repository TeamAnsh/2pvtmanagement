

import speech recognition as sr 
from googletrans import Translator 


def Listen():
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source) # Listening Mode.....
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="hi")
        query = str(query).lower()
        return query
    except Exception as e:
        print("Error:", str(e))
        return ""

Listen()



def Trans(Text):
    line = str(Text)
    translate = Translator()
    result = translate.translate(line)
    data = result.text
    print("You: ", data)
    return data
  

def MicExecution():
    query = Listen()
    data = TranslationHinToEng(query)
    return data


import pyttsx3

def speak(text):
    text_real = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 170)
    print("")
    print(f"> Hiroko: {text_real}")
    print("")
    engine.say(text_real)
    engine.runAndWait()

print(speak("Hello sir, I am your new assistant"))
