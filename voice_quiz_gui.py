import tkinter as tk
from tkinter import messagebox
from tkvideo import tkvideo
import pyttsx3, speech_recognition as sr
import threading, time, os, sys

quiz_data = [

    {"question": "Which planet is known as the Red Planet?",
     "options": ["Mercury", "Venus", "Earth", "Mars"],
     "answer": "mars"},

    {"question": "Who wrote Romeo and Juliet?",
     "options": ["William Shakespeare", "Charles Dickens", "Jane Austen", "Mark Twain"],
     "answer": "william shakespeare"},

    {"question": "What is the largest mammal?",
     "options": ["Elephant", "Blue Whale", "Hippopotamus", "Giraffe"],
     "answer": "blue whale"},

    {"question": "What is the capital of Australia?",
     "options": ["Sydney", "Melbourne", "Canberra", "Perth"],
     "answer": "canberra"},

    {"question": "Which gas do plants absorb from the atmosphere?",
     "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen"],
     "answer": "carbon dioxide"},

    {"question": "In what year did India gain independence?",
     "options": ["1945", "1946", "1947", "1948"],
     "answer": "1947"},

    {"question": "What is the chemical symbol for Gold?",
     "options": ["Au", "Ag", "Gd", "Go"],
     "answer": "au"},

    {"question": "Who is known as the father of computers?",
     "options": ["Alan Turing", "Bill Gates", "Charles Babbage", "Steve Jobs"],
     "answer": "charles babbage"},

    {"question": "Which language is used to create web pages?",
     "options": ["Python", "C++", "HTML", "Java"],
     "answer": "html"},

    {"question": "Which country is known as the Land of the Rising Sun?",
     "options": ["China", "India", "Japan", "South Korea"],
     "answer": "japan"},

]

engine = pyttsx3.init()
engine.setProperty("rate", 175)
recognizer = sr.Recognizer()

def speak(text):
    threading.Thread(target=lambda: engine.say(text) or engine.runAndWait(), daemon=True).start()

def listen():
    with sr.Microphone() as src:
        try:
            audio = recognizer.listen(src, timeout=5, phrase_time_limit=6)
            return recognizer.recognize_google(audio).lower()
        except:
            return None

class VoiceQuizApp:
    def __init__(self, root):
        self.root, self.idx, self.score = root, 0, 0
        root.title("AI Voice Quiz"); root.geometry("640x600")

        # Video
       # Video
        label = tk.Label(root)
        label.pack()
        
        video_path = r"C:\Users\LENOVO\OneDrive\Desktop\Project Folder\Quiz Platform Ai\robot.mp4"
        if not os.path.exists(video_path):
            sys.exit("❗ robot.mp4 NOT FOUND")
        
        self.video = tkvideo(video_path, label, loop=1, size=(600, 300))
        self.video.play()

        # Quiz
        self.q_label = tk.Label(root, font=("Arial", 14), wraplength=600)
        self.q_label.pack(pady=10)

        self.opt_var = tk.StringVar()
        self.opt_frame = tk.Frame(root); self.opt_frame.pack()

        tk.Button(root, text="🎤 Speak Answer", command=self.voice_answer).pack(pady=5)
        tk.Button(root, text="➡ Submit", command=self.submit_answer).pack(pady=3)

        self.status = tk.Label(root, font=("Arial", 12)); self.status.pack(pady=5)

        self.load_question()

    def load_question(self):
        self.status.config(text="")
        if self.idx >= len(quiz_data): return self.finish_quiz()

        q = quiz_data[self.idx]
        self.q_label.config(text=f"Q{self.idx+1}: {q['question']}")
        self.opt_var.set(None)

        for w in self.opt_frame.winfo_children(): w.destroy()
        for opt in q["options"]:
            tk.Radiobutton(self.opt_frame, text=opt, value=opt.lower(),
                           variable=self.opt_var, font=("Arial", 12)).pack(anchor="w")

        threading.Thread(target=self.read_question, daemon=True).start()

    def read_question(self):
        q = quiz_data[self.idx]
        speak(f"Question {self.idx+1}. {q['question']}")
        for i, opt in enumerate(q["options"], 1):
            speak(f"Option {i}. {opt}")
            time.sleep(0.2)

    def voice_answer(self):
        ans = listen()
        if ans: self.opt_var.set(ans)

    def submit_answer(self):
        sel = self.opt_var.get()
        if not sel:
            return messagebox.showwarning("No answer", "Please speak or select an answer.")
        correct = quiz_data[self.idx]["answer"]
        if correct in sel:
            self.score += 1
            self.status.config(text="✅ Correct!", fg="green")
            speak("Correct")
        else:
            self.status.config(text=f"❌ Wrong! Correct: {correct.title()}", fg="red")
            speak(f"The correct answer is {correct}")
        self.idx += 1
        self.root.after(2000, self.load_question)

    def finish_quiz(self):
        self.q_label.config(text=f"Quiz Over! Score: {self.score}/{len(quiz_data)}")
        self.opt_frame.pack_forget()
        self.status.pack_forget()
        speak(f"Quiz complete. You scored {self.score} out of {len(quiz_data)}.")

if __name__ == "__main__":
    root = tk.Tk()
    VoiceQuizApp(root)
    root.mainloop()
