© 2025 - Made by Dante Muller (https://github.com/ancan322)
# PCA - Personal Chat Assistant

Asistente de voz que escucha tu voz, la transcribe y responde usando ChatGPT y síntesis de voz (TTS).

Voice assistant in Spanish that hears your voice, transcribes it, and replies using ChatGPT and text-to-speech (TTS).

---

## Features

- Voice recognition in Spanish
- Conversations using the ChatGPT API
- Voice replies using Edge TTS
- Saves conversation history to a JSON file
- System tray icon
- Press the "K" key to start talking

---

## Requirements

- Python 3.10 or higher
- OpenAI API key

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/ancan322/PCAGitHub.git
cd PCAGitHub

2.Install dependencies
pip install -r requirements.txt

3.Set your OpenAI API key:
On Windows (CMD):
set OPENAI_API_KEY=your_api_key

On Linux/macOS (bash):
export OPENAI_API_KEY=your_api_key

4.Run it
python python PCAGitHub.py
