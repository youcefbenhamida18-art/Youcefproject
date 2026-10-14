import sys
import subprocess

print("Installing required packages...")
subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "moviepy", "Pillow", "google-api-python-client", "google-auth-oauthlib", "google-auth-httplib2"])

import os
import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from moviepy.editor import TextClip, ColorClip, CompositeVideoClip

def generate_video():
    print("Generating video...")
    bg = ColorClip(size=(1080, 1920), color=(20, 20, 40), duration=5)
    txt_clip = TextClip("Daily Riddle Challenge!\nCan you solve this?", fontsize=70, color='white', size=(1000, 1800), method='caption')
    txt_clip = txt_clip.set_pos('center').set_duration(5)
    video = CompositeVideoClip([bg, txt_clip])
    video.write_videofile("output_short.mp4", fps=24, codec='libx264', audio_codec='aac')
    print("Video created successfully!")
    return "output_short.mp4"

def get_credentials():
    token_json = os.environ.get('YOUTUBE_TOKEN')
    if token_json:
        return Credentials.from_authorized_user_info(json.loads(token_json), ['https://www.googleapis.com/auth/youtube.upload'])
    raise Exception("Token not found in secrets")

def upload_to_youtube(video_file, title, description):
    creds = get_credentials()
    youtube = build('youtube', 'v3', credentials=creds)
    body = {
        'snippet': {'title': title, 'description': description, 'tags': ['Shorts', 'Riddles'], 'categoryId': '22'},
        'status': {'privacyStatus': 'public', 'selfDeclaredMadeForKids': False}
    }
    media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
    response = youtube.videos().insert(part=','.join(body.keys()), body=body, media_body=media).execute()
    print(f"Uploaded! ID: {response.get('id')}")

if __name__ == "__main__":
    vid = generate_video()
    upload_to_youtube(vid, "Daily Riddle #Shorts", "Solve this riddle!")

