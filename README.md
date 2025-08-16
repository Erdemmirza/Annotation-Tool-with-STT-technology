# Annotation Tool with STT Technology

A media-player–like annotation tool that allows users to select segments in a video and 
automatically transcribe them into text using speech-to-text (STT) technology.

## System Requirements

Before running this project, make sure the following requirements are met:

- **Python ≥ 3.11**
- **FFmpeg** – Required for audio and video processing. FFmpeg must be installed on your system and added to your PATH.

## Installing FFmpeg

**Windows, MacOS, and Linux (Debian/Ubuntu) in one go:**

1. **Windows:** Download the zip from the [official FFmpeg site](https://ffmpeg.org/download.html) or [Gyan.dev builds](https://www.gyan.dev/ffmpeg/builds/), extract the zip and add the `bin` folder to your system PATH (e.g., `C:\ffmpeg\bin`).  
2. **MacOS (using Homebrew):** `brew install ffmpeg`  
3. **Linux (Debian/Ubuntu):** `sudo apt update && sudo apt install ffmpeg`  

4. Verify installation and install Python dependencies:
    ```
    ffmpeg -version
    pip install -r requirements.txt
## Python Dependencies(requirements.txt contents:)
    PySide6>=6.6
    openai-whisper>=20231117
    ffmpeg-python>=0.2.0


