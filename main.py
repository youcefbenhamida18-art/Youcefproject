import os
import random
from PIL import Image, ImageDraw
from moviepy import ImageClip

CONTENT_CATEGORIES = {
    "riddles": [
        {"q": "What has to be broken before you can use it?", "ans": "An egg"},
        {"q": "I speak without a mouth and hear without ears. What am I?", "ans": "An echo"}
    ],
    "did_you_know": [
        {"q": "Did you know a blue whale's heart is the size of a car?", "ans": "True!"},
        {"q": "What percentage of the human body is water?", "ans": "About 60%"}
    ]
}

def create_video_frame(question, answer):
    width, height = 1080, 1920
    image = Image.new("RGB", (width, height), color=(20, 24, 33))
    draw = ImageDraw.Draw(image)
    
    draw.text((100, 700), "DAILY TRIVIA & RIDDLES", fill=(255, 204, 0))
    draw.text((100, 900), f"Q: {question}", fill=(255, 255, 255))
    draw.text((100, 1100), f"Ans: {answer}", fill=(0, 255, 128))
    
    frame_path = "temp_frame.png"
    image.save(frame_path)
    return frame_path

def generate_short_video():
    category = random.choice(list(CONTENT_CATEGORIES.keys()))
    item = random.choice(CONTENT_CATEGORIES[category])
    
    print(f"Generating video for category: {category}")
    print(f"Question: {item['q']}")
    
    frame_path = create_video_frame(item['q'], item['ans'])
    
    clip = ImageClip(frame_path).set_duration(5)
    video_output = "output_short.mp4"
    clip.write_videofile(video_output, fps=24, codec="libx264", audio=False)
    
    print(f"Video successfully generated: {video_output}")

if __name__ == "__main__":
    generate_short_video()
