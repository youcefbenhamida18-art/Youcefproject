import os
import json
import subprocess
from PIL import Image, ImageDraw
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

def generate_video():
    print("Generating video frame with Pillow...")
    # إنشاء خلفية ملونة للشورتز بالمقاسات الصحيحة (1080x1920)
    img = Image.new('RGB', (1080, 1920), color=(20, 20, 40))
    d = ImageDraw.Draw(img)
    
    # النص الذي سيظهر في الفيديو
    text = "Daily Riddle Challenge!\nCan you solve this?"
    
    # رسم النص على الصورة
    d.text((250, 900), text, fill=(255, 255, 255))
    
    img_path = "riddle_frame.png"
    img.save(img_path)
    
    print("Converting image to video using ffmpeg...")
    # تحويل الصورة مباشرة إلى فيديو مدته 5 ثوانٍ باستخدام ffmpeg بدون أي مشاكل
    cmd = [
        "ffmpeg", "-loop", "1", "-i", img_path, 
        "-c:v", "libx264", "-t", "5", "-pix_fmt", "yuv420p", 
        "-y", "output_short.mp4"
    ]
    subprocess.run(cmd, check=True)
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
