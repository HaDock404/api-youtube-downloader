from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import yt_dlp
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
import uuid

# Initialisation de l'application FastAPI
app = FastAPI()


class VideoRequest(BaseModel):
    url: str


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)


@app.get("/")
def hello():
    """
    Default route to welcome users and direct them to documentation.

    Returns:
        dict: A welcome message.
    """

    return {"message": "Hi, add /docs to the URL to use the API."}


@app.post("/download")
async def download_video(request: VideoRequest):
    url = request.url

    # Générer un nom de fichier temporaire unique
    temp_filename = str(uuid.uuid4())
    output_file = f"{temp_filename}.mp4"

    ydl_opts = {
        'outtmpl': f"{temp_filename}.%(ext)s",  # Utilisation du nom temporaire
        'format': 'bestvideo+bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'webm',
        }],
    }

    try:
        # Télécharger la vidéo
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Rechercher le fichier téléchargé
        video_file = None
        for filename in os.listdir("."):
            if filename.startswith(temp_filename) and filename.endswith(".webm"):
                video_file = filename
                break

        if not video_file:
            raise HTTPException(status_code=500, detail="Failed to download video")

        # Convertir en .mp4
        clip = VideoFileClip(video_file)
        clip.write_videofile(output_file, codec="libx264", audio_codec="aac")
        clip.close()

        # Supprimer les fichiers temporaires
        os.remove(video_file)

        return {"message": "Conversion completed", "file": output_file}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")