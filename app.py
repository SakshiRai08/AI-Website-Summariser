import gradio as gr
import os
from bs4 import BeautifulSoup
from scraper import fetch_website_contents
from Summarizer import summarize_website

def get_summary(url):
    if not url.strip():
        return "⚠️ Please enter a valid URL."
    html = fetch_website_contents(url)
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text(separator=" ", strip=True)
    text = text[:10000]
    summary = summarize_website(text)
    return summary

with gr.Blocks(title="🔎 AI Website Summarizer") as app:
    gr.Markdown(
        """
        # 🌐 AI Website Summarizer
        Enter a website URL below, and get a concise summary of its content!
        """
    )

    with gr.Row():
        with gr.Column():
            url_input = gr.Textbox(
                label="🌐 Website URL",
                placeholder="https://en.wikipedia.org/wiki/AI")
            summarize_button = gr.Button("📝Summarize", variant="primary")

        with gr.Column():
            output = gr.Markdown(label="📝 Summary")
            summarize_button.click(fn=get_summary, inputs=url_input, outputs=output)
            url_input.submit(fn=get_summary, inputs=url_input, outputs=output)
            gr.Markdown("---\n*Tip: Works best with articles, blogs, docs, and news sites*")

app.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 10000)), theme=gr.themes.Soft())