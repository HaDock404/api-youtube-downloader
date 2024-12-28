import yt_dlp
from moviepy import VideoFileClip
import os

url = input("Enter video URL: ")

# Options pour yt-dlp
ydl_opts = {
    'format': 'bestvideo+bestaudio/best',  # Combine la meilleure vidéo et le meilleur audio
    'postprocessors': [{  # Fusionne audio et vidéo si nécessaire
        'key': 'FFmpegVideoConvertor',
        'preferedformat': 'webm',  # Format de sortie correct
    }],
}

# Télécharger la vidéo
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

for filename in os.listdir("."):
    if filename.endswith(".webm"):
        video_file = os.path.join(".", filename)
        output_file = "converted_video.mp4"

# Charger la vidéo
clip = VideoFileClip(video_file)

# Sauvegarder en .mp4
clip.write_videofile(output_file, codec="libx264", audio_codec="aac")
clip.close()

print(f"Conversion completed: {output_file}")
