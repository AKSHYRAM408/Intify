import time
import os
import requests
import streamlit as st
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from link import post_links  # ✅ Import Instagram post links

# ✅ Load API key from .env file
load_dotenv()
GROK_API_KEY = os.getenv("GROQ_API_KEY")

if not GROK_API_KEY:
    st.error("🚨 Error: GROK_API_KEY is not set. Check your .env file.")
    st.stop()

GROK_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# ✅ Function to scrape Instagram comments
def scrape_instagram_comments(reel_url):
    options = Options()
    options.add_argument("--headless")  
    options.add_argument("--disable-blink-features=AutomationControlled")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(reel_url)
    time.sleep(5)  

    comments_data = []
    
    comment_elements = driver.find_elements(By.CSS_SELECTOR, "ul li")

    for comment_element in comment_elements:
        try:
            comment = comment_element.find_element(By.CSS_SELECTOR, "span").text  
            comments_data.append(comment)
        except:
            continue  

    driver.quit()
    return comments_data

# ✅ Scrape comments from all posts
def get_all_comments():
    all_comments = {}
    for link in post_links:
        comments = scrape_instagram_comments(link)
        all_comments[link] = comments
    return all_comments

# ✅ Function to analyze comments and get mood-based song recommendations
def analyze_comments_and_suggest_songs(comment_text):
    messages = [
        {"role": "system", "content": "You are an expert AI that detects the overall mood from multiple comments and recommends songs based on that mood."},
        {"role": "user", "content": f"Analyze the following Instagram comments collectively:\n\n{comment_text}\n\n"
                                    "Dont print anything except mood found and song"
                                     "1. Detect the **overall sentiment** from all comments combined (happy, sad, neutral, relaxing, energetic).\n"
                                     "2. Consider **keywords** in the comments to improve song recommendations.\n"
                                     "3. Recommend **3 songs** in Tamil and English that match the detected sentiment.\n\n"
                                     "**Format response as:**\n"
                                     "- **Detected Mood**: (mood)\n"
                                     "- **Recommended Songs**:\n"
                                     "  1. Song Name - Artist\n"
                                     "  2. Song Name - Artist\n"
                                     "  3. Song Name - Artist"}
    ]

    payload = {
        "model": "llama3-8b-8192",
        "messages": messages,
        "temperature": 0.3,
        "max_tokens": 300
    }

    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(GROK_API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response from AI.")
    else:
        return f"Error: {response.status_code} - {response.text}"

# ✅ Spotify-Themed UI
st.set_page_config(page_title="🎵 INTIFY", page_icon="🎧", layout="wide")

# 🎨 Custom Spotify-like UI
st.markdown(
    """
    <style>
        body {
            background-color: #121212;
            color: white;
            font-family: 'Arial', sans-serif;
        }
        .title {
            text-align: center;
            font-size: 40px;
            font-weight: bold;
            color: #1DB954;
        }
        .subtitle {
            text-align: center;
            font-size: 18px;
            color: #B3B3B3;
        }
        .box {
            background-color: #181818;
            padding: 20px;
            border-radius: 10px;
        }
        .footer {
            text-align: center;
            color: #B3B3B3;
            font-size: 14px;
        }
        .success-box {
            background-color: #1DB954;
            color: black;
            padding: 15px;
            border-radius: 10px;
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 class='title'>🎵 INTIFY - Emotion-Based Song Recommender</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Dive Deep into music</p>", unsafe_allow_html=True)

# ✅ Scraping & Analyzing
with st.spinner("⏳ Scraping comments and analyzing mood..."):
    all_comments = get_all_comments()
    combined_comments = "\n".join([comment for comments in all_comments.values() for comment in comments])
    ai_response = analyze_comments_and_suggest_songs(combined_comments)

# ✅ Display Results in a Styled Box
st.markdown("<h3 style='color: #1DB954;'>🎶Recommended Songs 🎶</h3>", unsafe_allow_html=True)
st.markdown(f"<div class='success-box'>{ai_response}</div>", unsafe_allow_html=True)

# ✅ Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p class='footer'>Developed by Deepthinkers </p>", unsafe_allow_html=True)
