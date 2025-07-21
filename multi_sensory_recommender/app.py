import streamlit as st
from recommender.utils import get_weather, get_local_time
from recommender.ml_predict import predict_ml
from deepface import DeepFace
import numpy as np
import cv2
import requests

def display_context(context):
    st.markdown("""
    <style>
    .context-card {
        background-color: #f6f9fc;
        border-radius: 12px;
        padding: 1.2em 1em 0.5em 1em;
        margin-bottom: 1.5em;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    </style>
    """, unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="context-card">', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🏙️ City", context.get("city", "-"))
        col2.metric("🌦️ Weather", context.get("weather", "-").capitalize())
        col3.metric("🕒 Time of Day", context.get("time_of_day", "-").capitalize())
        col4.metric("😊 Emotion", context.get("emotion", "-").capitalize())
        st.markdown('</div>', unsafe_allow_html=True)

st.set_page_config(page_title="Multi-Sensory Content Recommender", layout="wide")
st.title("🌟 Multi-Sensory Content Recommender")
st.markdown("""
Welcome! Get personalized movie, music, and food recommendations based on your mood, weather, and time of day.
""")

OPENWEATHER_API_KEY = st.secrets.get("OPENWEATHER_API_KEY")
if not OPENWEATHER_API_KEY:
    st.error("OpenWeather API key not found. Please add it to your Streamlit secrets.")
    st.stop()

# --- TMDB API Connectivity Test ---
TMDB_API_KEY = st.secrets.get("TMDB_API_KEY")
if not TMDB_API_KEY:
    st.error("TMDB API key not found. Please add it to your Streamlit secrets.")
    st.stop()

tmdb_test_url = "https://api.themoviedb.org/3/search/movie"
tmdb_test_params = {"api_key": TMDB_API_KEY, "query": "happy"}
try:
    tmdb_test_response = requests.get(tmdb_test_url, params=tmdb_test_params, timeout=10)
    if tmdb_test_response.status_code == 200:
        st.success("TMDB API connectivity: Success ✅")
    else:
        st.error(f"TMDB API connectivity: Failed ❌ (Status {tmdb_test_response.status_code})")
        st.error(tmdb_test_response.text)
except Exception as e:
    st.error(f"TMDB API connectivity: Exception ❌ {e}")

# --- Input Section ---
with st.container():
    col1, col2, col3 = st.columns([2, 2, 2])
    with col1:
        city = st.text_input("🏙️ Enter your city for weather updates:")
    with col2:
        emotion = st.selectbox("😊 How are you feeling?", ["happy", "sad", "neutral"])
    with col3:
        img_file = st.camera_input("📸 Or take a picture to detect your emotion")

context = {}
if city:
    weather = get_weather(city, OPENWEATHER_API_KEY)
    if isinstance(weather, dict) and "error" in weather:
        st.error(f"Could not get weather for {city}: {weather['error']}")
        weather_main = "clear"
    elif isinstance(weather, dict) and "main" in weather:
        weather_main = weather["main"]
    else:
        st.error(f"Unexpected weather data format for {city}.")
        weather_main = "clear"
    local_time = get_local_time()
    import datetime
    hour = int(local_time.split()[1].split(":")[0])
    if 5 <= hour < 12:
        time_of_day = "morning"
    elif 12 <= hour < 17:
        time_of_day = "afternoon"
    elif 17 <= hour < 21:
        time_of_day = "evening"
    else:
        time_of_day = "night"
    detected_emotion = None
    if img_file is not None:
        file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)
        st.image(img, channels="BGR", caption="Your photo")
        try:
            result = DeepFace.analyze(img, actions=["emotion"], enforce_detection=False)
            detected_emotion = result[0]['dominant_emotion']
            st.success(f"Detected Emotion: {detected_emotion}")
        except Exception as e:
            st.error(f"Error: {e}")
    final_emotion = detected_emotion if detected_emotion else emotion
    context = {
        "city": city,
        "weather": weather_main.lower(),
        "time_of_day": time_of_day,
        "emotion": final_emotion
    }
    display_context(context)
    if st.button("✨ Get Recommendations", use_container_width=True):
        recs = predict_ml(context)
        st.subheader("🎬 Movie Recommendations")
        if isinstance(recs, dict) and 'movie' in recs and isinstance(recs['movie'], list):
            movie_cols = st.columns(3)
            for idx, movie in enumerate(recs['movie']):
                with movie_cols[idx % 3]:
                    if isinstance(movie, dict):
                        if movie.get('poster_url'):
                            st.image(movie['poster_url'], width=180)
                        st.markdown(f"**{movie.get('title', 'No Title')}**")
                        st.caption(movie.get('overview', ''))
                    else:
                        st.write("Movie item is not a dict:", movie)
        else:
            st.info("No movie recommendations available.")
        st.subheader("🎵 Music Recommendations")
        if isinstance(recs, dict) and 'music' in recs and isinstance(recs['music'], list):
            music_cols = st.columns(3)
            for idx, track in enumerate(recs['music']):
                with music_cols[idx % 3]:
                    if isinstance(track, dict):
                        if track.get('album_art'):
                            st.image(track['album_art'], width=120)
                        st.markdown(f"**{track.get('title', 'No Title')}** by {track.get('artist', 'Unknown')}")
                        if track.get('album_name'):
                            st.caption(f"Album: {track['album_name']}")
                        if track.get('preview_url'):
                            st.markdown(f"[▶️ Preview Track]({track['preview_url']})")
                        if track.get('spotify_url'):
                            st.markdown(f"[Open in Spotify]({track['spotify_url']})")
                    else:
                        st.write("Music item is not a dict:", track)
        else:
            st.info("No music recommendations available.")
        st.subheader("🍲 Food Recommendations")
        if isinstance(recs, dict) and 'food' in recs and isinstance(recs['food'], list):
            food_cols = st.columns(3)
            for idx, food in enumerate(recs['food']):
                with food_cols[idx % 3]:
                    if isinstance(food, dict):
                        if food.get('image'):
                            st.image(food['image'], width=120)
                        st.markdown(f"**{food.get('title', 'No Title')}**")
                        if food.get('source_url'):
                            st.markdown(f"[View Recipe]({food['source_url']})")
                    else:
                        st.write("Food item is not a dict:", food)
        else:
            st.info("No food recommendations available.")
else:
    st.info("Please enter your city to get started.") 