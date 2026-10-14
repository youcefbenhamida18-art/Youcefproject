import os
import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Load client secret from GitHub Secrets
client_secret_data = os.environ.get("CLIENT_SECRET")

if client_secret_data:
    with open("client_secret.json", "w") as f:
        f.write(client_secret_data)

# Load token from GitHub Secrets if available
youtube_token_data = os.environ.get("YOUTUBE_TOKEN")

if youtube_token_data:
    with open("token.json", "w") as f:
        f.write(youtube_token_data)

def upload_to_youtube(video_file, title, description):
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
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
    # Example call to test upload after video generation
    upload_to_youtube("output_short.mp4", "Daily Riddle Challenge! #Shorts", "Can you solve this riddle? Write your answer in the comments!")
