import os
import random

# A diverse database of content categories to ensure variety and prevent repetition
CONTENT_CATEGORIES = {
    "riddles": [
        {"q": "What has to be broken before you can use it?", "ans": "An egg"},
        {"q": "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?", "ans": "An echo"}
    ],
    "did_you_know": [
        {"q": "Did you know that a blue whale's heart is about the size of what?", "ans": "A small car"},
        {"q": "Did you know what percentage of the human body is made of water?", "ans": "About 60 percent"}
    ],
    "history_trivia": [
        {"q": "History Quiz: Which Ottoman Sultan conquered Constantinople?", "ans": "Mehmed the Conqueror"},
        {"q": "History Quiz: Who was the first President of the United States?", "ans": "George Washington"}
    ]
}

def generate_smart_content():
    # Randomly select a category to ensure endless variety
    category_name = random.choice(list(CONTENT_CATEGORIES.keys()))
    item = random.choice(CONTENT_CATEGORIES[category_name])
    
    print(f"--- Smart Dynamic Content Generator ---")
    print(f"Category: {category_name}")
    print(f"Question: {item['q']}")
    print(f"Answer: {item['ans']}")
    print(f"Status: Ready for video rendering and automated publishing.")
    print("---------------------------------------")

if __name__ == "__main__":
    generate_smart_content()
