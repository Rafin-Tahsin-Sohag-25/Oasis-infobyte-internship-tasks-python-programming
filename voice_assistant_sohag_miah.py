import datetime
import os
import smtplib
import time
from urllib.parse import quote
import webbrowser

import pyautogui
import pyttsx3
import speech_recognition as sr
import wikipedia

class DesktopAssistant:
    def __init__(self, assistant_name="Hunterdii"):
        self.name = assistant_name
        self.contacts = {
            "friend": "friend@example.com",
            "family": "family@example.com"
        }
        # Initialize TTS Engine
        self.tts_engine = pyttsx3.init('sapi5')
        system_voices = self.tts_engine.getProperty('voices')
        if len(system_voices) > 1:
            self.tts_engine.setProperty('voice', system_voices[1].id)

    def speak_text(self, text_content):
        """Converts text to speech output."""
        self.tts_engine.say(text_content)
        self.tts_engine.runAndWait()

    def greet_user(self):
        """Greets user according to current system time."""
        current_hour = datetime.datetime.now().hour
        
        if 0 <= current_hour < 12:
            time_greeting = "Good Morning!"
        elif 12 <= current_hour < 18:
            time_greeting = "Good Afternoon!"
        else:
            time_greeting = "Good Evening!"

        self.speak_text(time_greeting)
        self.speak_text(f"I am {self.name}. How can I assist you today?")

    def capture_voice_input(self):
        """Captures microphone input and returns recognized text."""
        recognizer_instance = sr.Recognizer()
        
        with sr.Microphone() as mic_source:
            print("Listening for commands...")
            recognizer_instance.pause_threshold = 1.0
            captured_audio = recognizer_instance.listen(mic_source)

        try:
            print("Processing voice input...")
            user_command = recognizer_instance.recognize_google(captured_audio, language='en-in')
            print(f"Recognized: {user_command}\n")
            return user_command.lower()
        except Exception:
            print("Audio not clear. Please repeat.")
            return "none"

    def dispatch_email(self, recipient_addr, message_body):
        """Sends email using SMTP protocol."""
        smtp_user = os.environ.get("MY_EMAIL", "your_email@gmail.com")
        smtp_pass = os.environ.get("MY_PASSWORD", "your_app_password")

        with smtplib.SMTP('smtp.gmail.com', 587) as mail_server:
            mail_server.ehlo()
            mail_server.starttls()
            mail_server.login(smtp_user, smtp_pass)
            mail_server.sendmail(smtp_user, recipient_addr, message_body)

    def execute_command_loop(self):
        """Main listening and execution loop."""
        self.greet_user()
        
        while True:
            cmd = self.capture_voice_input()

            if 'none' in cmd:
                continue

            # Information Retrieval
            if 'wikipedia' in cmd:
                self.speak_text('Searching Wikipedia resources...')
                clean_query = cmd.replace("wikipedia", "").strip()
                try:
                    summary_result = wikipedia.summary(clean_query, sentences=2)
                    self.speak_text("According to Wikipedia")
                    print(summary_result)
                    self.speak_text(summary_result)
                except Exception:
                    self.speak_text("Unable to retrieve information from Wikipedia.")

            # Web Navigation
            elif 'open youtube' in cmd:
                webbrowser.open("https://youtube.com")

            elif 'open google' in cmd:
                webbrowser.open("https://google.com")

            elif 'play music' in cmd:
                playlist_link = "https://music.youtube.com/playlist?list=PLIL965-SXjbVEiWwe1l6RApWYDnbhc_Oz"
                webbrowser.open(playlist_link)
                time.sleep(5)
                pyautogui.press('space')

            elif 'the time' in cmd:
                formatted_time = datetime.datetime.now().strftime("%H:%M:%S")
                self.speak_text(f"Sir, the time is {formatted_time}")

            elif 'open code' in cmd:
                script_path = r"C:\Users\hetpa\OneDrive\Desktop\Python Programs\server.py"
                if os.path.exists(script_path):
                    os.startfile(script_path)
                else:
                    self.speak_text("Target file path does not exist.")

            # Search Operations
            elif 'search google for' in cmd:
                keyword = cmd.replace('search google for', '').strip()
                webbrowser.open(f"https://www.google.com/search?q={quote(keyword)}")

            elif 'search youtube for' in cmd:
                keyword = cmd.replace('search youtube for', '').strip()
                webbrowser.open(f"https://www.youtube.com/results?search_query={quote(keyword)}")

            elif 'search in hindi for' in cmd:
                keyword = cmd.replace('search in hindi for', '').strip()
                webbrowser.open(f"https://www.google.com/search?hl=hi&q={quote(keyword)}")

            elif 'search in gujarati for' in cmd:
                keyword = cmd.replace('search in gujarati for', '').strip()
                webbrowser.open(f"https://www.google.com/search?hl=gu&q={quote(keyword)}")

            # Communication & Utilities
            elif 'send email' in cmd:
                try:
                    self.speak_text("Who is the recipient?")
                    target_person = self.capture_voice_input().strip()
                    target_email = self.contacts.get(target_person)

                    if target_email:
                        self.speak_text("What should I write?")
                        email_text = self.capture_voice_input()
                        self.dispatch_email(target_email, email_text)
                        self.speak_text("Email dispatched successfully!")
                    else:
                        self.speak_text("Contact not found in dictionary.")
                except Exception as err:
                    print(err)
                    self.speak_text("Failed to send email.")

            elif 'open notepad' in cmd:
                os.system("start notepad.exe")

            elif 'open calculator' in cmd:
                os.system("start calc.exe")

            elif 'open command prompt' in cmd:
                os.system("start cmd.exe")

            # System Operations
            elif 'exit' in cmd or 'stop' in cmd or 'bye' in cmd:
                self.speak_text("Shutting down assistant services. Goodbye!")
                break

            elif 'shutdown' in cmd:
                self.speak_text("Initiating system shutdown.")
                os.system("shutdown /s /t 1")

            elif 'restart' in cmd:
                self.speak_text("Rebooting the operating system.")
                os.system("shutdown /r /t 1")

if __name__ == "__main__":
    bot = DesktopAssistant()
    bot.execute_command_loop()