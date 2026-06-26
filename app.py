import os
import gradio as gr
from google import genai

# Gemini setup
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
chat = client.chats.create(model="gemini-2.5-flash")

# store chat history
history_store = []

def chat_fn(message, history):
    global history_store

    try:
        response = chat.send_message(message)
        reply = response.text

        # store history
        history_store.append((message, reply))

        return reply
    except Exception as e:
        return f"Error: {e}"


def clear_chat():
    global history_store
    history_store = []
    return []


def build_ui():
    with gr.Blocks(theme=gr.themes.Soft()) as demo:

        gr.Markdown("# 🧠 Ghajini AI")

        with gr.Row():

            # Sidebar
            with gr.Column(scale=1):
                gr.Markdown("## 📚 Chats")
                chat_list = gr.List(label="History", value=[])

                clear_btn = gr.Button("🗑 Clear Chat")

            # Main Chat
            with gr.Column(scale=4):
                chatbot = gr.Chatbot(height=500)
                msg = gr.Textbox(placeholder="Type your message...")

                send = gr.Button("🚀 Send")

        # Events
        send.click(chat_fn, inputs=msg, outputs=chatbot)
        clear_btn.click(clear_chat, outputs=chatbot)

    return demo


demo = build_ui()

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
