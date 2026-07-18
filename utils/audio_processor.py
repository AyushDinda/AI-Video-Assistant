import yt_dlp
from pydub import AudioSegment
import os
import shutil

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# FFmpeg auto-detection
# Probes PATH first, then the winget install directory as a fallback so the
# binary is found even if the shell PATH hasn't been refreshed after install.
# ---------------------------------------------------------------------------
def _find_ffmpeg() -> str | None:
    found = shutil.which("ffmpeg")
    if found:
        return os.path.dirname(found)

    winget_pkgs = os.path.join(
        os.environ.get("LOCALAPPDATA", ""),
        "Microsoft", "WinGet", "Packages"
    )
    if os.path.isdir(winget_pkgs):
        for entry in os.scandir(winget_pkgs):
            if entry.is_dir() and entry.name.lower().startswith("gyan.ffmpeg"):
                for root, _, files in os.walk(entry.path):
                    if "ffmpeg.exe" in files:
                        return root

    for base in [r"C:\Program Files\ffmpeg\bin", r"C:\ffmpeg\bin"]:
        if os.path.isfile(os.path.join(base, "ffmpeg.exe")):
            return base

    return None


FFMPEG_DIR = _find_ffmpeg()
if FFMPEG_DIR is None:
    raise RuntimeError(
        "ffmpeg not found. Install it with:  winget install --id Gyan.FFmpeg\n"
        "Then open a NEW terminal so the PATH update takes effect."
    )

# Tell pydub where ffmpeg lives (suppresses the RuntimeWarning)
AudioSegment.converter = os.path.join(FFMPEG_DIR, "ffmpeg.exe")
AudioSegment.ffmpeg    = os.path.join(FFMPEG_DIR, "ffmpeg.exe")
AudioSegment.ffprobe   = os.path.join(FFMPEG_DIR, "ffprobe.exe")


def download_youtube_audio(url: str) -> str:
    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "ffmpeg_location": FFMPEG_DIR,
        "quiet": True,
    }
    # Only use cookies.txt if it exists in the project root (avoids crash when absent)
    if os.path.isfile("cookies.txt"):
        ydl_opts["cookiefile"] = "cookies.txt"
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).replace(".webm", ".wav").replace(".m4a", ".wav")
    return filename


def convert_to_wav(input_path: str) -> str:
    """Convert any audio/video file to WAV format using pydub."""
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000)  # 16kHz mono
    audio.export(output_path, format="wav")
    return output_path


def chunk_audio(wav_path: str, chunk_minutes: int = 10) -> list:
    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = chunk_minutes * 60 * 1000

    chunks = []

    for i, start in enumerate(range(0, len(audio), chunk_ms)):
        chunk = audio[start: start + chunk_ms]
        chunk_path = f"{wav_path}_chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)

    return chunks


def process_input(source: str) -> list:
    if source.startswith("http://") or source.startswith("https://"):
        print("Detected YouTube URL. Downloading audio...")
        wav_path = download_youtube_audio(source)
    else:
        print("Detected local file. Converting to WAV...")
        wav_path = convert_to_wav(source)

    print("Chunking audio...")
    chunks = chunk_audio(wav_path)
    print(f"Audio ready — {len(chunks)} chunk(s) created.")
    return chunks
