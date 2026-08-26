import os
import gradio as gr
from openai import OpenAI

# Connect to Groq
client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def ask_ai(message, history):
    try:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are GWMS, the AI assistant for Fikky Work Place. "
                    "Be helpful, clear, accurate, and friendly. "
                    "If you don't know something, say so instead of making it up."
                )
            }
        ]

        # Add previous conversation
        for item in history:
            if isinstance(item, dict):
                role = item.get("role")
                content = item.get("content")

                if role in ["user", "assistant"] and isinstance(content, str):
                    messages.append({
                        "role": role,
                        "content": content
                    })

        # Add current question
        messages.append({
            "role": "user",
            "content": message
        })

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"GWMS AI connection error: {str(e)}"


with gr.Blocks(
    title="GWMS | Fikky Work Place"
) as app:

    gr.Markdown("""
# 🤖 GWMS

## FIKKY WORK PLACE

**Your Personal AI Assistant**
""")

    gr.ChatInterface(
        fn=ask_ai,
        title="💬 GWMS CHAT",
        description="Ask GWMS anything"
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))

    app.launch(
        server_name="0.0.0.0",
        server_port=port
    )
