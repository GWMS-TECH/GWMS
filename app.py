import gradio as gr

def ask_ai(message, history):
    return "GWMS is online! 🤖 Your AI assistant is being connected."

with gr.Blocks(title="GWMS | Fikky Work Place") as app:

    gr.Markdown(
        """
        # 🤖 GWMS
        ## FIKKY WORK PLACE
        **Your Personal AI Assistant**
        """
    )

    gr.ChatInterface(
        fn=ask_ai,
        title="💬 GWMS CHAT",
        description="Welcome to Fikky Work Place"
    )

if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=7860
    )
