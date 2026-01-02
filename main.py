import uuid
import subprocess
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, HTMLResponse
import imageio_ffmpeg

app = FastAPI()

@app.get("/")
def home():
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.post("/convert")
async def convert(file: UploadFile = File(...)):
    uid = str(uuid.uuid4())
    input_path = f"/tmp/{uid}.mp4"
    output_path = f"/tmp/{uid}.mp3"

    # scrittura a chunk
    with open(input_path, "wb") as f:
        while chunk := await file.read(1024*1024):
            f.write(chunk)

    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
    # conversione MP4 → MP3
    subprocess.run([
        ffmpeg_path, "-y",
        "-i", input_path,
        "-vn",
        "-ab", "128k",
        "-ar", "44100",
        "-f", "mp3",
        output_path
    ], check=True)

    return FileResponse(
        output_path,
        media_type="audio/mpeg",
        filename="audio.mp3"
    )