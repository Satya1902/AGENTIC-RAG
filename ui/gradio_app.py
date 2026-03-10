
import gradio as gr
import requests


from src.config import get_settings
from src.agent.agent import agentic_app

async def ask_agent(question):

    settings = get_settings()
    base_url = settings.base_url
    port = settings.port
    url = f"{base_url}:{port}"

    # res = requests.post(
    #     f"{url}/query",
    #     json={"question": question}
    # )
    res = await agentic_app(question)
    print("response from gradio is ------------------------------------: ",res)
    # return res.get("Answer", "No answer received")
    return res

    # return res.json().get("Answer", "No answer received")


# Custom dark styling
custom_css = """
.gradio-container {
    background: #0f172a !important;
}

#title {
    text-align: center;
    font-size: 34px;
    font-weight: bold;
    color: #e2e8f0;
}

#subtitle {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 25px;
}

textarea {
    background: #1e293b !important;
    color: #e2e8f0 !important;
    border: 1px solid #334155 !important;
    font-size: 16px !important;
}

#ask-btn {
    background: linear-gradient(90deg,#6366f1,#3b82f6);
    color: white;
    font-weight: 600;
    border-radius: 8px;
}

#ask-btn:hover {
    background: linear-gradient(90deg,#4f46e5,#2563eb);
}

footer {
    visibility: hidden;
}
"""


dark_theme = gr.themes.Default(
    primary_hue="blue",
    neutral_hue="slate"
)


with gr.Blocks(
    theme=dark_theme,
    css=custom_css,
    title="Agentic RAG Assistant"
) as demo:

    gr.Markdown(
        """
        <div id="title">🤖 Agentic RAG Assistant</div>
        <div id="subtitle">
        Hybrid Retrieval • Gemini • Agent Tools
        </div>
        """
    )

    with gr.Column():

        question = gr.Textbox(
            label="Ask your question",
            placeholder="Example: Compare SBI and HDFC home loan interest rates",
            lines=5
        )

        ask_button = gr.Button("Ask to Agent", elem_id="ask-btn")

        answer = gr.Textbox(
            label="Agent Response",
            lines=12
        )

    ask_button.click(
        fn=ask_agent,
        inputs=question,
        outputs=answer
    )

    gr.Markdown(
        """
        ---
        ⚡ **Powered by FastAPI • Gemini • Hybrid RAG**
        """
    )


demo.launch(
    server_name="0.0.0.0",
    server_port=3000
)