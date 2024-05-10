import tkinter as tk
from tkinter import ttk
import threading
import speech_recognition as sr
import pyperclip

class VoiceToTextConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice to Text Converter")
        self.root.geometry("600x400")
        self.root.configure(bg="#a9a9a9")

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Helvetica", 12), foreground="black", background="black")

        self.text_entry = tk.Text(root, height=10, width=50, bg="#d3d3d3", fg="black", font=("Helvetica", 12))
        self.text_entry.grid(row=0, column=0, padx=20, pady=20, columnspan=2, sticky="nsew")

        self.start_button = ttk.Button(root, text="Start", command=self.start_conversion, style="TButton")
        self.start_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.stop_button = ttk.Button(root, text="Stop", command=self.stop_conversion, state=tk.DISABLED, style="TButton")
        self.stop_button.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

        self.copy_button = ttk.Button(root, text="Copy", command=self.copy_text, style="TButton")
        self.copy_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.quit_button = ttk.Button(root, text="Quit", command=root.quit, style="TButton")
        self.quit_button.grid(row=2, column=1, padx=20, pady=10, sticky="ew")

        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000  # Adjust this value to set the energy threshold
        self.recognizer.pause_threshold = 0.8    # Adjust this value to set the pause threshold
        self.is_listening = False

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_rowconfigure(2, weight=0)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def start_conversion(self):
        self.is_listening = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        threading.Thread(target=self.convert_speech_to_text).start()

    def stop_conversion(self):
        self.is_listening = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def convert_speech_to_text(self):
        while self.is_listening:
            with sr.Microphone() as source:
                print("Listening...")
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source)
            if not self.is_listening:
                break
            try:
                text = self.recognizer.recognize_google(audio)
                self.text_entry.delete(1.0, tk.END)
                self.text_entry.insert(tk.END, text)
            except sr.UnknownValueError:
                self.text_entry.delete(1.0, tk.END)
                self.text_entry.insert(tk.END, "Could not understand audio.")
            except sr.RequestError as e:
                self.text_entry.delete(1.0, tk.END)
                self.text_entry.insert(tk.END, "Could not request results; {0}".format(e))

    def copy_text(self):
        text_to_copy = self.text_entry.get("1.0", tk.END).strip()
        if text_to_copy:
            pyperclip.copy(text_to_copy)

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceToTextConverter(root)
    root.mainloop()
