import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser
import os
import wikipedia

# Initialize the pyttsx3 engine for speech
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def greet_user():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good morning!")
    elif hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")

    speak("I am your virtual assistant. How can I help you today?")

def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        print("Sorry, the speech service is down.")
        return ""
    return command.lower()

def open_website(website):
    speak(f"Opening {website}")
    webbrowser.open(f"https://{website}.com")

def close_website():
    speak("Closing the website.")
    os.system("taskkill /f /im chrome.exe")  # This works for Chrome, modify for other browsers if necessary.

def tell_time():
    time = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"The current time is {time}")

def search_wikipedia(query):
    speak(f"Searching Wikipedia for {query}")
    try:
        result = wikipedia.summary(query, sentences=2)
        speak(result)
        print(result)
    except wikipedia.exceptions.DisambiguationError as e:
        speak("There are multiple results for that. Let me search more specifically.")
        print(e.options)
        # You can add logic here to handle disambiguation, e.g., choosing the first option.
    except wikipedia.exceptions.HTTPTimeoutError:
        speak("There was an issue with the Wikipedia search. Please try again later.")
        print("Timeout error.")
    except wikipedia.exceptions.RedirectError:
        speak("The query redirected to another page. I couldn't find the specific answer.")
        print("Redirect error.")
    except Exception as e:
        speak("Sorry, I couldn't find any results.")
        print(f"Error: {e}")

def stop_assistant():
    speak("Assistant is stopping. Goodbye!")
    print("Assistant is stopping.")
    exit()

def assistant_info(command):
    if "who are you" in command or "tell me about you" in command:
        info = """
        I am a virtual assistant powered by Python. I am here to help you with various tasks, 
        such as telling the time, opening websites, searching Wikipedia, and much more. 
        My goal is to make your life easier and assist you in completing your tasks efficiently.
        """
        speak(info)
        print(info)
    elif "what can you do" in command or "what are your capabilities" in command:
        capabilities = """
        I can assist you in the following ways:
        - Tell you the current time.
        - Open websites based on your commands.
        - Search Wikipedia for any topic.
        - Provide information about myself when asked.
        - And much more! Just ask, and I will try my best to help you.
        """
        speak(capabilities)
        print(capabilities)
    elif "help" in command or "assist me" in command:
        help_info = """
        Here are some things I can do for you:
        - Ask for the time.
        - Ask me to open a website (e.g., "Open YouTube").
        - Ask me to search something on Wikipedia (e.g., "Search Python").
        - Ask me about myself (e.g., "Who are you?").
        - Say 'exit' or 'quit' to stop the assistant.
        """
        speak(help_info)
        print(help_info)
    else:
        speak("Sorry, I didn't understand your request.")
        print("Sorry, I didn't understand your request.")

def main():
    greet_user()

    while True:
        command = listen_command()

        if "time" in command:
            tell_time()

        elif "open" in command:
            website = command.split("open")[-1].strip()
            open_website(website)

        elif "search" in command:
            query = command.split("search")[-1].strip()
            search_wikipedia(query)

        elif "who are you" in command or "tell me about you" in command or "assistant info" in command:
            assistant_info(command)  # Provides information about the assistant

        elif "close website" in command or "close the website" in command:
            close_website()  # Close the website if requested

        elif "stop" in command or "exit" in command or "quit" in command:
            stop_assistant()  # Call stop_assistant() to stop the assistant

        elif "ask" in command:
            query = command.split("ask")[-1].strip()
            search_wikipedia(query)  # Search for any question asked

if __name__ == "__main__":
    main()
