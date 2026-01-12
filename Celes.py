# Celes.py
import os
import json
import requests
from openai import OpenAI

# Placeholder imports for voice
try:
    import pyttsx3
except:
    pyttsx3 = None

try:
    import speech_recognition as sr
except:
    sr = None

# ================= CONFIG =================
BOT_NAME = "Celes"

OPENAI_API_KEY = "YOUR_OPENAI_KEY"
GOOGLE_API_KEY = "YOUR_GOOGLE_KEY"
GOOGLE_CX = "YOUR_GOOGLE_CX"

client = OpenAI(api_key=OPENAI_API_KEY)

MEMORY_FILE = "memory.json"

# ================= MEMORY =================
def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {"personal": {}, "facts": {}}
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)

memory = load_memory()

# ================= GOOGLE SEARCH =================
def google_search(query):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_CX,
        "q": query,
        "num": 3
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        data = r.json()
        if "items" not in data:
            return "I couldn't find reliable results."
        results = [item["snippet"] for item in data["items"]]
        return "\n".join(results)
    except:
        return "Search failed due to network issues."

# ================= OPENAI CHAT =================
def chat_with_ai(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"You are {BOT_NAME}, a friendly personal AI assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# ================= VOICE PLACEHOLDERS =================
tts_engine = None
if pyttsx3:
    try:
        tts_engine = pyttsx3.init()
    except:
        tts_engine = None

def speak(text):
    if tts_engine:
        # Strip emojis
        clean_text = ''.join(c for c in text if ord(c) < 10000)
        tts_engine.say(clean_text)
        tts_engine.runAndWait()

def listen():
    if sr:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
        try:
            return r.recognize_google(audio)
        except:
            return ""
    return ""

# ================= MAIN BRAIN =================
def get_bot_reply(user_text):
    text = user_text.lower()

    # Detailed search only if explicitly requested
    if text.startswith("/search") or text.startswith("slash search"):
        query = user_text.replace("/search", "").replace("slash search", "").strip()
        result = google_search(query)
        return f"I found this online:\n{result}"

    # Short conversational answers
    if any(word in text for word in ["who is", "do you know", "what is", "tell me about"]):
        reply = chat_with_ai(user_text)
        return f"{reply}\nDo you want more details?"

    # Normal conversation
    return chat_with_ai(user_text)