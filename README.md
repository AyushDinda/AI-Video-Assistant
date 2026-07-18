# 🎬 AI Video Assistant

An intelligent video processing application that extracts audio from YouTube videos or local files, transcribes it (with support for English and Hinglish translation), generates professional summaries, extracts action items, and allows you to chat with the content using Retrieval-Augmented Generation (RAG).

## ✨ Features

- **YouTube & Local File Support:** Simply paste a YouTube URL or provide a local video/audio file path.
- **Dual Language Support:** 
  - **English:** Uses local OpenAI Whisper for fast, accurate transcription.
  - **Hinglish:** Uses the Sarvam AI API to seamlessly transcribe and translate Hinglish audio into English.
- **Smart Summarization:** Powered by Mistral AI via LangChain to generate titles, detailed summaries, action items, key decisions, and open questions.
- **Interactive RAG Chat:** Ask questions directly against the video transcript using a local vector database (ChromaDB + HuggingFace Embeddings).
- **Beautiful UI:** A sleek, animated, and responsive user interface built with Streamlit.

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Audio Processing:** `yt-dlp`, `pydub`, `ffmpeg`
- **Transcription:** OpenAI Whisper (Local), Sarvam AI (API)
- **LLM Orchestration:** LangChain (LCEL)
- **Large Language Model:** Mistral (`mistral-small-latest`)
- **Vector Database:** ChromaDB
- **Embeddings:** HuggingFace (`all-MiniLM-L6-v2`)

## 🚀 Local Installation

### Prerequisites
- Python 3.11+
- FFmpeg installed on your system (Required for `pydub` audio processing).

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/video-assistant.git
cd video-assistant
```

### 2. Create a virtual environment
```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On Mac/Linux
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up API Keys
Create a `.env` file in the root directory and add your API keys:
```env
MISTRAL_API_KEY=your_mistral_api_key_here
SARVAM_API_KEY=your_sarvam_api_key_here
```

### 5. Run the Application
```bash
streamlit run app.py
```
The app will open automatically in your browser at `http://localhost:8501`.

## ☁️ Deployment (Streamlit Community Cloud)

This project is pre-configured for deployment on Streamlit Community Cloud.

1. Push this repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io/).
3. Click **New app** and select your repository.
4. Set the Main file path to `app.py`.
5. Click **Advanced Settings** and add your secrets:
   ```toml
   MISTRAL_API_KEY="your_mistral_api_key_here"
   SARVAM_API_KEY="your_sarvam_api_key_here"
   ```
6. Click **Deploy**.

*(Note: The included `packages.txt` ensures that Streamlit installs `ffmpeg` on their Linux servers automatically).*

## ⚠️ Notes on Hardware Requirements
Processing long YouTube videos requires downloading the audio and running Whisper/Chroma locally. If running on free cloud tiers (like Streamlit Cloud with ~1GB RAM), extremely long videos might cause memory limits to be exceeded.

## 📜 License
MIT License
