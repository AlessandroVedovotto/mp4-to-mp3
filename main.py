from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, HTMLResponse
import subprocess
import uuid
import os
import tempfile

app = FastAPI()

# Homepage
@app.get("/")
def home():
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

# Conversione MP4 → MP3
@app.post("/convert")
async def convert(file: UploadFile = File(...)):
    uid = str(uuid.uuid4())
    temp_dir = tempfile.gettempdir()  # percorso sicuro Windows/macOS
    input_path = os.path.join(temp_dir, f"{uid}.mp4")
    output_path = os.path.join(temp_dir, f"{uid}.mp3")

    # scrittura file a chunk (1MB)
    with open(input_path, "wb") as f:
        while chunk := await file.read(1024*1024):
            f.write(chunk)

    # conversione con FFmpeg
    # assicurati di avere FFmpeg installato e accessibile dal PATH
    subprocess.run([
        "ffmpeg", "-y",
        "-i", input_path,
        "-vn",           # no video
        "-ab", "128k",   # bitrate audio
        "-ar", "44100",  # sample rate
        "-f", "mp3",
        output_path
    ], check=True)

    # restituisce MP3 completo
    response = FileResponse(
        output_path,
        media_type="audio/mpeg",
        filename="audio.mp3"
    )

    # opzionale: pulizia dopo invio
    # puoi scommentare per non occupare spazio
    # import threading
    # threading.Thread(target=lambda: (os.remove(input_path), os.remove(output_path))).start()

    return response
