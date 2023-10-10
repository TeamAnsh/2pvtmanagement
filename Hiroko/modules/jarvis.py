import openai
import pyttsx3
import speech recognition as sr 
from googletrans import Translator 




def Listen():
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="hi")
        query = str(query).lower()
        return query
    except Exception as e:
        print("Error:", str(e))
        return ""



def Trans(Text):
    line = str(Text)
    translate = Translator()
    result = translate.translate(line)
    data = result.text
    print("You: ", data)
    return data
  



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
     









openai.api_key = "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"



def chatgpt(x):
    a = message.text.split(' ', 1)[1]
    MODEL = "gpt-3.5-turbo"
    resp = openai.ChatCompletion.create(model=MODEL,messages=[{"role": "user", "content": a}],
    temperature=0.2)
    x=resp['choices'][0]["message"]["content"]
    speak(x)



def MicExecution():
    query = Listen()
    data = Trans(query)
    x = chatgpt(data)
    return x
    
    
speak(MicExecution())
