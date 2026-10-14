import os
import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from moviepy.editor import TextClip, ColorClip, CompositeVideoClip

def generate_video():
    print("جاري إنشاء فيديو اللغز تلقائياً...")
    # إنشاء خلفية ملونة للفيديو (مقاس شورتس: عرض 1080 وطول 1920، لمدة 5 ثواني)
    bg = ColorClip(size=(1080, 1920), color=(20, 20, 40), duration=5)
    
    # إضافة نص اللغز (يمكنك تعديل النص واللون حسب رغبتك)
    txt_clip = TextClip("Daily Riddle Challenge!\nCan you solve this?", fontsize=70, color='white', size=(1000, 1800), method='caption')
    txt_clip = txt_clip.set_pos('center').set_duration(5)
    
    # دمج الخلفية مع النص
    video = CompositeVideoClip([bg, txt_clip])
    
    # حفظ الفيديو الناتج بالاسم المطلوب
    output_filename = "output_short.mp4"
    video.write_videofile(output_filename, fps=24, codec='libx264', audio_codec='aac')
    print("تم إنشاء الفيديو بنجاح باسم:", output_filename)
    return output_filename

def get_credentials():
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    token_json = os.environ.get('YOUTUBE_TOKEN')
    if token_json:
        token_data = json.loads(token_json)
        return Credentials.from_authorized_user_info(token_data, SCOPES)
    raise Exception("خطأ: لم يتم العثور على التوكن YOUTUBE_TOKEN في GitHub Secrets")

def upload_to_youtube(video_file, title, description):
    creds = get_credentials()
    youtube = build('youtube', 'v3', credentials=creds)

    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': ['Shorts', 'Riddles', 'Quiz'],
            'categoryId': '22'
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False
        }
    }

    media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part=','.join(body.keys()), body=body, media_body=media)

    response = request.execute()
    print(f"Video uploaded successfully! Video ID: {response.get('id')}")

if __name__ == "__main__":
    # الخطوة 1: توليد الفيديو تلقائياً
    video_path = generate_video()
    
    # الخطوة 2: رفع الفيديو الناتج إلى يوتيوب
    upload_to_youtube(video_path, "Daily Riddle Challenge! #Shorts", "Can you solve this riddle? Write your answer in the comments!")
