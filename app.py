import speech_recognition as sr
import pyttsx3
import requests
import datetime
import webbrowser
import time

# Initialize TTS engine
engine = pyttsx3.init()

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

# Listen for voice command
def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)

        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio)
            print("You said:", command)
            return command.lower()

        except:
            return ""

# Weather Function
def get_weather(city):
    api_key = "06578f21cf343ffa1fb9d647c4734b64"

    city = city.strip()

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url).json()

        print("City:", city)
        print("Response:", response)

        if str(response.get("cod")) == "200":
            temp = response["main"]["temp"]
            weather = response["weather"][0]["description"]

            speak(f"Temperature is {temp} degree Celsius")
            speak(f"Weather is {weather}")
        else:
            speak("City not found")
            print("Error:", response.get("message"))

    except Exception as e:
        print("Error:", e)
        speak("Unable to fetch weather information.")

# Global variable
latest_news = []

# News Function
def get_news():
    global latest_news

    api_key = "694076811f77465bb35d84bf952a256c"

    url = f"https://newsapi.org/v2/everything?q=India&language=en&sortBy=publishedAt&apiKey={api_key}"

    try:
        response = requests.get(url).json()

        if response.get("status") != "ok":
            speak("Unable to fetch news.")
            print("Error:", response)
            return

        articles = response.get("articles", [])[:5]

        if not articles:
            speak("No news articles found.")
            return

        latest_news = articles

        speak("Here are today's top headlines")

        for i, article in enumerate(articles, start=1):
            title = article.get("title", "No title available")

            print(f"Headline {i}: {title}")

            speak(f"Headline {i}")
            speak(title)

    except Exception as e:
        print("News Error:", e)
        speak("An error occurred while fetching news.")

# Reminder Function
def set_reminder():
    speak("Enter reminder message")
    message = input("Reminder: ")

    speak("Enter time in seconds")
    seconds = int(input("Seconds: "))

    time.sleep(seconds)

    speak("Reminder Alert")
    speak(message)


# Main Assistant
def assistant():

    speak("Hello, I am your personal assistant")

    while True:

        command = listen()

        if "time" in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {current_time}")

        elif "date" in command:
            today = datetime.date.today()
            speak(f"Today's date is {today}")

        elif any(word in command for word in ["weather", "wether", "whether", "vedar"]):
            speak("Please tell city name")
            city = listen()
            get_weather(city)

        elif "news" in command:
            get_news()

        elif "open youtube" in command:
            webbrowser.open("https://www.youtube.com")
            speak("Opening YouTube")

        elif "open google" in command:
            webbrowser.open("https://www.google.com")
            speak("Opening Google")

        elif "reminder" in command:
            set_reminder()
        
        elif "first news" in command:
            if latest_news:
                speak(latest_news[0]["title"])
            else:
                speak("No news available.")

        elif "second news" in command:
            if len(latest_news) >= 2:
                speak(latest_news[1]["title"])
            else:
                speak("No second news available.")

        elif "exit" in command or "stop" in command:
            speak("Goodbye")
            break

assistant()