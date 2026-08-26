import os
import base64
import gradio as gr
from openai import OpenAI


# ============================================================
# FIKYA AI ASSISTANT
# ============================================================

# Get Groq API key from Render Environment Variables
api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    raise RuntimeError(
        "GROQ_API_KEY is missing. Add it in Render → Environment."
    )


# Connect to Groq
client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)


# ============================================================
# BACKGROUND IMAGE
# ============================================================

def get_background():

    image_path = "background.png"

    if not os.path.exists(image_path):
        return ""

    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(
            image_file.read()
        ).decode("utf-8")

    return f"data:image/png;base64,{encoded}"


background = get_background()


# ============================================================
# AI FUNCTION
# ============================================================

def ask_ai(message, history):

    try:

        messages = [
            {
                "role": "system",
                "content": """
You are FIKYA, a smart, helpful and friendly AI assistant.

Your job is to help users with:
- General questions
- Learning
- Technology
- Business
- Writing
- Research
- Coding
- Everyday problems

Give clear, useful and accurate answers.

Do not pretend to know something when you do not know it.

Keep answers easy to understand while still being intelligent and helpful.

Your name is FIKYA.
"""
            }
        ]


        # Add previous conversation
        if history:

            for item in history:

                # Gradio messages format
                if isinstance(item, dict):

                    role = item.get("role")
                    content = item.get("content")

                    if (
                        role in ["user", "assistant"]
                        and isinstance(content, str)
                    ):
                        messages.append({
                            "role": role,
                            "content": content
                        })

                # Older Gradio tuple format
                elif isinstance(item, (list, tuple)):

                    if len(item) >= 2:

                        user_message = item[0]
                        assistant_message = item[1]

                        if user_message:
                            messages.append({
                                "role": "user",
                                "content": str(user_message)
                            })

                        if assistant_message:
                            messages.append({
                                "role": "assistant",
                                "content": str(assistant_message)
                            })


        # Add current question
        messages.append({
            "role": "user",
            "content": message
        })


        # Ask AI
        response = client.chat.completions.create(

            model="openai/gpt-oss-20b",

            messages=messages,

            temperature=0.7,

            max_tokens=1200
        )


        return response.choices[0].message.content


    except Exception as error:

        return (
            "Sorry, FIKYA encountered a connection problem.\n\n"
            f"Error: {str(error)}"
        )


# ============================================================
# CUSTOM DESIGN
# ============================================================

css = f"""

/* MAIN PAGE */

.gradio-container {{
    max-width: 1200px !important;
    margin: auto !important;

    background:
        linear-gradient(
            rgba(2, 8, 20, 0.78),
            rgba(2, 8, 20, 0.88)
        ),
        url("{background}");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;

    min-height: 100vh;
}}


/* HEADER */

#fikya-header {{
    text-align: center;
    padding: 25px 10px 10px 10px;
}}


#fikya-title {{
    font-size: 48px !important;
    font-weight: 800 !important;
    letter-spacing: 4px;

    color: #ffffff;

    text-shadow:
        0 0 10px #168cff,
        0 0 25px #168cff,
        0 0 45px #168cff;
}}


#fikya-subtitle {{
    color: #b8d9ff;

    font-size: 16px;

    letter-spacing: 2px;
}}


/* CHAT AREA */

#chatbot {{
    border-radius: 20px !important;

    background: rgba(5, 15, 30, 0.72) !important;

    backdrop-filter: blur(14px);

    border: 1px solid rgba(60, 160, 255, 0.35);

    box-shadow:
        0 0 25px rgba(0, 130, 255, 0.18),
        inset 0 0 30px rgba(0, 100, 255, 0.04);
}}


/* MESSAGE BOX */

textarea {{
    background: rgba(5, 15, 30, 0.85) !important;

    color: white !important;

    border: 1px solid rgba(50, 150, 255, 0.4) !important;

    border-radius: 15px !important;
}}


/* BUTTONS */

button {{
    border-radius: 12px !important;
}}


/* FOOTER */

#fikya-footer {{
    text-align: center;

    color: rgba(190, 220, 255, 0.7);

    font-size: 12px;

    padding: 10px;
}}
"""


# ============================================================
# GRADIO APP
# ============================================================

with gr.Blocks(
    title="FIKYA | AI Assistant",
    css=css
) as app:

    # Header

    gr.HTML(
        """
        <div id="fikya-header">

            <div id="fikya-title">
                FIKYA
            </div>

            <div id="fikya-subtitle">
                YOUR INTELLIGENT AI ASSISTANT
            </div>

        </div>
        """
    )


    # Chatbot

    chatbot = gr.Chatbot(
        height=560,
        elem_id="chatbot",
        type="messages"
    )


    # Chat interface

    gr.ChatInterface(
        fn=ask_ai,
        chatbot=chatbot,
        textbox=gr.Textbox(
            placeholder="Ask FIKYA anything...",
            container=True
        ),
        title="",
        description=""
    )


    # Footer

    gr.HTML(
        """
        <div id="fikya-footer">
            Powered by FIKYA AI
        </div>
        """
    )


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    port = int(
        os.environ.get("PORT", 7860)
    )

    app.launch(
        server_name="0.0.0.0",
        server_port=port
    )
