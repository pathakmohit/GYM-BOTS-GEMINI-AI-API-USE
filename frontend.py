import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
import random
import json
import webbrowser
import datetime
import requests  # For calling the Gemini AI API


''' Defining the Chatbot GUI Class '''
class ChatbotGUI:
    def __init__(self, master):
        self.master = master
        self.setup_gui()
        self.conversation_history = []
        # Place your API key here
        self.api_key = "AIzaSyBZKYFtsGq_V0C7VZ0W1EkwCg0hBXvlCmo"


    def setup_gui(self):
        self.master.title("GYM-BOT")
        self.master.geometry("500x600")
        self.master.configure(bg="#f0f0f0")

        style = ttk.Style()
        style.theme_use("clam")

        main_frame = ttk.Frame(self.master, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ''' Chat History Text Box '''
        self.chat_history = scrolledtext.ScrolledText(
            main_frame, wrap=tk.WORD, width=60, height=25, font=("Arial", 10)
        )
        self.chat_history.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.chat_history.config(state=tk.DISABLED)

        ''' Input and Button Frames '''
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=5)

        self.user_input = ttk.Entry(input_frame, width=50, font=("Arial", 10))
        self.user_input.pack(side=tk.LEFT, padx=(0, 5), expand=True, fill=tk.X)
        self.user_input.bind("<Return>", lambda event: self.send_message())

        self.send_button = ttk.Button(
            input_frame, text="Send", command=self.send_message
        )
        self.send_button.pack(side=tk.RIGHT)

        ''' Button Frame for Clear, Save, and Help '''
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)

        self.clear_button = ttk.Button(
            button_frame, text="Clear Chat", command=self.clear_chat
        )
        self.clear_button.pack(side=tk.LEFT, padx=(0, 5))

        self.save_button = ttk.Button(
            button_frame, text="Save Chat", command=self.save_chat
        )
        self.save_button.pack(side=tk.LEFT)

        self.help_button = ttk.Button(
            button_frame, text="Help", command=self.show_help
        )
        self.help_button.pack(side=tk.RIGHT)

    def send_message(self):
        user_message = self.user_input.get()
        self.user_input.delete(0, tk.END)

        if user_message:
            self.update_chat_history(f"You: {user_message}")
            bot_response = self.chatbot_response(user_message)
            self.update_chat_history(f"Bot: {bot_response}")
            self.conversation_history.append((user_message, bot_response))

    def update_chat_history(self, message):
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, message + "\n\n")
        self.chat_history.see(tk.END)
        self.chat_history.config(state=tk.DISABLED)

    def chatbot_response(self, user_message):
        if user_message.lower() in ["exit", "quit", "bye"]:
            return "Goodbye, it was nice chatting with you."
        elif user_message.lower().startswith("search "):
            query = user_message[7:]
            webbrowser.open(f"https://www.google.com/search?q={query}")
            return f"I've opened a web search for '{query}'."
        elif user_message.lower() == "time":
            return f"Current time is {datetime.datetime.now().strftime('%H:%M:%S')}"
        else:
            # Call the Gemini API instead of the local model
            return self.get_gemini_response(user_message)

    def get_gemini_response(self, user_message):
         # Gemini API endpoint (replace with your project ID)
        api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

        headers = {
            "x-goog-api-key": self.api_key,  # Gemini API Key from self.api_key
            "Content-Type": "application/json"
        }
        data = {
            "contents": [{
                "parts": [{
                    "text": user_message
                }]
            }]
        }
        try:
          # Make the request to Gemini API
            response = requests.post(api_url, headers=headers, json=data)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

            try:
                # Parse the JSON response
                response_data = response.json()
                # Get the text output from the first candidate
                candidates = response_data.get("candidates",[])
                if candidates:
                  output_text = candidates[0].get("content", {}).get("parts", [])[0].get("text")
                  return output_text
                else:
                    return "No response from Gemini" #Handle case with no candidates
            except json.JSONDecodeError:
               return f"Error decoding JSON response: {response.text}"
        except requests.exceptions.RequestException as e:
           #Handles all requests related errors including ConnectionError
           return f"Error calling Gemini AI API: {e}"

    def clear_chat(self):
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.delete(1.0, tk.END)
        self.chat_history.config(state=tk.DISABLED)
        self.conversation_history.clear()

    def save_chat(self):
        filename = (
            f"chat_history_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        with open(filename, "w") as f:
            for user_msg, bot_msg in self.conversation_history:
                f.write(f"You: {user_msg}\n")
                f.write(f"Bot: {bot_msg}\n\n")
        messagebox.showinfo("Chat Saved", f"Chat history has been saved to {filename}")

    def show_help(self):
        help_text = """
        Welcome to the GYM-BOT!

        Special Commands:
        - Type 'exit', 'quit', or 'bye' to end the conversation.
        - Type 'search <query>' to open a web search.
        - Type 'time' to get the current time.

        Features:
        - Clear Chat: Clears the current conversation.
        - Save Chat: Saves the conversation history to a file.
        - Help: Shows this help message.

        Enjoy chatting!
        """
        messagebox.showinfo("Chatbot Help", help_text)


if __name__ == "__main__":
    root = tk.Tk()
    ChatbotGUI(root)
    root.mainloop()