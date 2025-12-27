Zara – Intelligent Voice Assistant
Zara is a local, offline-first intelligent voice assistant built in Python.
It uses speech recognition, intent parsing, and a locally running LLM (Ollama) to respond to voice commands in real time.
The project focuses on system integration rather than just AI — combining audio input, background scheduling, UI state handling, and local inference.

Features: -
- Wake-word based activation (“Zara”)
- Real-time microphone input with visual listening meter
- Speech-to-text using Whisper
- Intent detection for common commands
- Fallback to Ollama for open-ended questions
- Streaming LLM responses (no long waiting)
- Floating UI pill showing assistant state (idle / listening / thinking / speaking)
- Alarms and reminders with background scheduler
- Fully local execution (no cloud APIs required)

Tech Stack: - 
- Python
- Whisper for speech recognition
- Ollama for local LLM responses
- FastAPI for internal state communication
- PyQt6 for lightweight UI
- SoundDevice / NumPy / SciPy for audio processing

How It Works (High Level): - 
- Zara listens for a wake word
- Records voice input after activation
- Transcribes audio using Whisper
- Tries to resolve intent locally
- Falls back to Ollama for general questions
- Speaks the response and updates UI state

Running the Project: - 
1. Start Ollama (in a separate terminal): ollama serve
Make sure a model is pulled, for example: ollama pull llama3

2. Install Python dependencies
pip install -r requirements.txt

3. Run the assistant
python -m app.main

Say “Zara” to activate.

Notes: -
- Ollama runs as a background service and is not installed via pip
- The macOS .app bundle build was attempted but intentionally excluded from final submission due to platform limitations
- The assistant is designed for local experimentation and learning, not production deployment

Project Status: -
- Core functionality is complete and stable.
- Future improvements may include better intent confidence handling and cross-platform UI packaging.
