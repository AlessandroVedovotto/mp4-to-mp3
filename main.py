from fastapi import FastAPI, UploadFile
import shutil
import os
import subprocess
import imageio_ffmpeg


app = FastAPI()

@app.post("/convert")
async def convert(file: UploadFile):
    uid = "tempfile"  # puoi usare uuid
    input_path = f"/tmp/{uid}.mp4"
    output_path = f"/tmp/{uid}.mp3"

    # Salva MP4
    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Usa ffmpeg-static per il path completo
    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

    # Converti in MP3
    subprocess.run([
        ffmpeg_path, "-y",
        "-i", input_path,
        "-vn",
        "-ab", "128k",
        "-ar", "44100",
        "-f", "mp3",
        output_path
    ], check=True)

    # Restituisci il file
    from fastapi.responses import FileResponse
    return FileResponse(output_path, media_type="audio/mpeg", filename="output.mp3")
