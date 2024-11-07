import google.generativeai as genai
import os
from dotenv import load_dotenv
import gradio as gr

load_dotenv()
print(os.getenv("GEMINI_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat()


def gradio_wrapper(message, _history):
    response = chat.send_message(message)
    return response.text


chat_interface = gr.ChatInterface(gradio_wrapper)
chat_interface.launch()
