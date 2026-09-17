# AudioMinutes

An AI-powered meeting minutes generator that converts audio recordings into structured meeting notes using speech-to-text and LLMs.

## How It Works

```text
Audio File
    ↓
Groq Whisper
    ↓
Transcript
    ↓
Gemini
    ↓
Structured JSON
    ↓
JSON Schema Validation
    ↓
Gradio Interface
```

## Features

* 🎙️ Convert meeting audio into text using Groq Whisper
* 🤖 Generate structured meeting minutes using Gemini
* 📝 Extract:

  * Meeting title
  * Summary
  * Key decisions
  * Action items
  * Action item owners
  * Due dates
  * Open questions
* ✅ Validate generated output using JSON Schema
* 🖥️ Simple Gradio web interface
* 🎧 Supports audio file input
* 🔐 API keys stored securely using environment variables

## Tech Stack

* **Python**
* **Groq Whisper** — Speech-to-text
* **Google Gemini** — Meeting summarization
* **Gradio** — Web interface
* **JSON Schema** — Output validation
* **PyDub** — Audio processing
* **OpenAI Python SDK** — API client for OpenAI-compatible endpoints
* **python-dotenv** — Environment variable management

## Project Structure

```text
AudioMinutes/
│
├── main.py
├── samples/
│   ├── Sample voice.mp3
│   └── voice2.mp3
├── .gitignore
└── README.md
```

> `.env` is intentionally excluded from the repository because it contains API keys.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Sunny-projects-05/audio-minutes.git
cd audio-minutes
```

### 2. Create a virtual environment

Using `uv`:

```bash
uv venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
uv pip install openai gradio pydub python-dotenv jsonschema
```

### 4. Configure API keys

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
GEMINI_API_KEY=your_gemini_api_key
```

You will need API access for:

* Groq Whisper
* Google Gemini

Never commit your `.env` file to GitHub.

## Run the Application

Start the application with:

```bash
python main.py
```

Gradio will launch the application locally.

Open the local URL shown in the terminal, typically:

```text
http://127.0.0.1:7860
```

## Example Workflow

1. Upload an audio recording.
2. Audio is sent to Groq Whisper for transcription.
3. The transcript is passed to Gemini.
4. Gemini generates structured meeting information.
5. The response is parsed as JSON.
6. JSON Schema validates the generated structure.
7. The transcript and structured minutes are displayed in Gradio.

## Example Output

The generated meeting minutes follow this structure:

```json
{
  "title": "Project Planning Meeting",
  "summary": "The team discussed the upcoming project milestones and development timeline.",
  "decisions": [
    "The team agreed to finalize the initial prototype this week."
  ],
  "action_items": [
    {
      "task": "Complete the prototype",
      "owner": "Team Member",
      "due": "Friday"
    }
  ],
  "open_questions": [
    "Which deployment platform should be used?"
  ]
}
```

## Current Limitations

This is **Version 1** of the project.

Current limitations include:

* No speaker diarization
* Long audio processing is not yet fully optimized with chunking
* Action-item extraction can occasionally miss implicitly assigned tasks
* Meeting titles and summaries depend on LLM output quality
* The interface is intentionally simple

## Future Improvements

Planned improvements for future versions:

* Long-audio chunking and transcript merging
* Better action-item extraction
* Editable meeting minutes
* Markdown export
* Improved error handling
* More polished Gradio interface
* Speaker identification/diarization
* Additional output formats

## Learning & Inspiration

This project was built while learning LLM application development and was inspired by concepts from **Ed Donner's LLM Engineering course**.

The project focuses on understanding the complete flow of an LLM application rather than relying on a large framework:

```text
Input → AI Processing → Structured Output → Validation → User Interface
```

## Version

**V1.0 — Initial working release**

Built with Python and free/hosted AI APIs as a hands-on LLM engineering project.
