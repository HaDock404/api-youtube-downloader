from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from jose import JWTError, jwt
import yt_dlp
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
import uuid

# === CONFIG JWT ===
SECRET_KEY = "dev-secret-key"  # à changer en prod
ALGORITHM = "HS256"

# === INIT APP ===
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


# === JWT DEPENDENCY ===
def verify_token(authorization: str = Header(...)):
    """
    Vérifie le token JWT passé dans le header Authorization: Bearer <token>
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    token = authorization[7:]  # Remove "Bearer "

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # facultatif, ici tu peux extraire les infos du user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


@app.get("/")
def hello():
    return {"message": "Hi, add /docs to the URL to use the API."}


@app.post("/download")
async def download_video(request: VideoRequest, token_data=Depends(verify_token)):
    url = request.url

    temp_filename = str(uuid.uuid4())
    output_file = f"{temp_filename}.mp4"

    ydl_opts = {
        'outtmpl': f"{temp_filename}.%(ext)s",
        'format': 'bestvideo+bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'webm',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        video_file = None
        for filename in os.listdir("."):
            if filename.startswith(temp_filename) and filename.endswith(".webm"):
                video_file = filename
                break

        if not video_file:
            raise HTTPException(status_code=500, detail="Failed to download video")

        clip = VideoFileClip(video_file)
        clip.write_videofile(output_file, codec="libx264", audio_codec="aac")
        clip.close()

        os.remove(video_file)

        return {"message": "Conversion completed", "file": output_file}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")