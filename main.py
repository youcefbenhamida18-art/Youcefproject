import os
import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

def get_credentials():
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    
    # 1. حاول القراءة من السر YOUTUBE_TOKEN المضاف في GitHub Secrets
    youtube_token = os.environ.get("YOUTUBE_TOKEN")
    if youtube_token:
        token_data = json.loads(youtube_token)
        return Credentials.from_authorized_user_info(token_data, SCOPES)
        
    # 2. في حال وجود ملف محلي token.json
    if os.path.exists('token.json'):
        return Credentials.from_authorized_user_file('token.json', SCOPES)
        
    raise Exception("لم يتم العثور على YOUTUBE_TOKEN في Secrets! يرجى إضافة التوكن.")

def upload_to_youtube(video_file, title, description):
    creds = get_credentials()
    youtube = build('youtube', 'v3', credentials=creds)
    
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': ['Shorts', 'Riddles', 'Trivia', 'Quiz'],
            'categoryId': '27'
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
    upload_to_youtube("output_short.mp4", "Daily Riddle Challenge! #Shorts", "Can you solve this riddle? Write your answer in the comments!")
