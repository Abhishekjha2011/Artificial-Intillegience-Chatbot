import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import smtplib
import webbrowser
import os
import requests
from bs4 import BeautifulSoup


# Initialize speech recognizer and engine
r = sr.Recognizer()
engine = pyttsx3.init()

# Define function to speak text
def speak(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

# Define function to recognize speech
def recognize_speech():
    with sr.Microphone() as source:
        
        speak("Tell me How can I help you...")
        
        audio = r.listen(source)
    try:
        # Use Google Speech Recognition API to transcribe audio
        text = r.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
    except sr.RequestError:
        speak("Sorry, speech service is unavailable.")
    return ""

# Define function to get current time
def get_time():
    now = datetime.datetime.now()
    speak(f"The current time is.. {now.strftime('%I:%M %p')}")

# Define function to get current date
def get_date():
    now = datetime.datetime.now()
    speak(f"Today is {now.strftime('%A, %B %d, %Y')}")

# Define function to search Google
def search_google(query):
    speak(f"Searching Google for {query}...")
    pywhatkit.search(query)

# Define function to get news headlines
def get_news():
    url = "https://news.google.com/rss"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="xml")
    items = soup.findAll('item')[:5]
    speak("Here are the top 5 headlines.")
    for item in items:
        speak(item.title.text)

# Define function to send WhatsApp message
def send_whatsapp_message():
    speak("What should I send?")
    message = recognize_speech()
    speak("When should I send it?")
    time = recognize_speech()
    hour, minute = time.split()
    hour = int(hour)
    minute = int(minute)
    pywhatkit.sendwhatmsg("+1234567890", message, hour, minute)

# Define function to open Gmail
def open_gmail():
    speak("Opening Gmail...")
    webbrowser.open("https://mail.google.com")

# Define function to send email
def send_email():
    speak("Who should I send it to?")
    recipient = recognize_speech()
    speak("What is the subject?")
    subject = recognize_speech()
    speak("What should I say?")
    body = recognize_speech()

    # Replace with your own email and password
    email = "your_email@gmail.com"
    password = "your_password"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)

    message = f"Subject: {subject}\n\n{body}"
    server.sendmail(email, recipient, message)

    server.quit()
    speak("Email sent!")

# Main loop
speak("Hello I'm Personal Assistent AI made by Tauqueer Alam, Utsav Kumar, Anup Kumar")
while True:
    command = recognize_speech().lower()
    if "hello" in command:
        speak("Hello! How can I assist you?")
    elif "time" in command:
        get_time()
    elif "date" in command:
        get_date()
    elif "google search" in command:
        query = command.replace("google search ", "")
        search_google(query)
    elif "news" in command:
        get_news()
    elif "send whatsapp message" in command:
        send_whatsapp_message()
    elif "open gmail" in command:
        open_gmail
    elif "thank you" in command:
        speak("You're welcome!")
    elif "stop" in command:
        speak("Goodbye!")
        exit()