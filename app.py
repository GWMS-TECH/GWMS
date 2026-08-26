import os
import gradio as gr

def ask_ai(message, history):
    return "GWMS is online. AI connection is the next step."

with gr.Blocks(title="GWMS | Fikky Work Place") as app:

    gr.Markdown("""
# 🤖 GWMS
## FIKKY WORK PLACE

**Your Personal AI Assistant**
""")

    gr.ChatInterface(
        fn=ask_ai,
        title="💬 GWMS CHAT",
        description="Your personal AI assistant"
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))

    app.launch(
        server_name="0.0.0.0",
        server_port=port
    )
