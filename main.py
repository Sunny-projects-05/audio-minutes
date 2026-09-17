from openai import OpenAI
import os
import json
from pathlib import Path
import gradio as gr
import pydub
from dotenv import load_dotenv
from jsonschema import validate, ValidationError


load_dotenv()

groq=OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

gemini=OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "summary": {"type": "string"},
        "decisions": {"type": "array", "items": {"type": "string"}},
        "action_items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "task": {"type": "string"},
                    "owner": {"type": "string"},
                    "due": {"type": "string"}
                },
                "required": ["task", "owner", "due"]
            }
        },
        "open_questions": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["title", "summary", "decisions", "action_items", "open_questions"]
}



def transcribe_audio(audio_path):
    with open(audio_path,"rb") as audio_file:
        transcription = groq.audio.transcriptions.create(
            model="whisper-large-v3-turbo",
            file=audio_file
        )
    transcript=transcription.text
    return transcript


def summarize_meeting(transcript):
    text=gemini.chat.completions.create(
        model="gemini-3.6-flash",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an assistant that summarizes meetings. "
                    "Return valid JSON only. Do not include Markdown, explanations, or text before/after the JSON. "
                    "The JSON must have this structure:\n"
                    "{\n"
                    '  "title": "string",\n'
                    '  "summary": "string",\n'
                    '  "decisions": ["string", ...],\n'
                    '  "action_items": [\n'
                    "    {\n"
                    '      "task": "string",\n'
                    '      "owner": "string",\n'
                    '      "due": "string"\n'
                    "    }\n"
                    "  ],\n"
                    '  "open_questions": ["string", ...]\n'
                    "}"
                )
            },
            {
                "role": "user",
                "content": f"Summarize this meeting: {transcript}"
            }
        ]
    )
    generated=text.choices[0].message.content
    answer=json.loads(generated)
    return answer

def validate_summary(summary):

    try:
        authentic=validate(instance=summary, schema=schema)
        return summary

    except ValidationError as Err:
        print("❌ Conflict occured : ", Err)
        return None


def process_meeting(audio_path):
    transcript=transcribe_audio(audio_path)
    result=summarize_meeting(transcript)
    summary=validate_summary(result)
    
    return transcript, summary

# outcome = gr.Interface(
#     fn=process_meeting,
#     inputs=gr.Audio(type="filepath"),   
#     outputs=[
#         gr.Textbox(label="Transcript"), 
#         gr.JSON(label="Summary")        
#     ]
# ).launch(server_name="127.0.0.1")

# def create_markdown(summary):
#     title = summary["title"]
#     summarised=summary["summary"]
#     decisions=summary["decisions"]
#     task=summary[["action_items"]["task"]]
#     owner=summary[["action_items"]["owner"]]
#     due=summary[["action_items"]["due"]]
#     open_questions=summary["open_questions"]



with gr.Blocks() as demo:
    gr.Markdown("## 🎙️ Meeting Transcriber & Summarizer")

    with gr.Row():
        audio_input = gr.Audio(type="filepath", label="Upload Meeting Audio")

    with gr.Row():
        transcript_output = gr.Textbox(label="Transcript", lines=10)
        summary_output = gr.JSON(label="Summary")

    run_button = gr.Button("Process Meeting")

    run_button.click(
        fn=process_meeting,
        inputs=audio_input,
        outputs=[transcript_output, summary_output]
    )

demo.launch(server_name="127.0.0.1")