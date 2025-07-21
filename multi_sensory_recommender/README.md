# Multi-Sensory Content Recommender

A web app that recommends movies, music, and food based on time of day, weather, and facial emotion detection.

## Features
- Movie, music, and food recommendations
- Personalization using:
  - Time of day
  - Weather (via OpenWeatherMap)
  - Facial emotion detection (DeepFace)
- Built with Streamlit for a fast, beautiful UI

## Setup
1. Clone the repo
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Get an OpenWeatherMap API key and add it to `app.py`
4. Run the app:
   ```bash
   streamlit run app.py
   ```

## Current Progress
- [x] Weather and time-based context input
- [ ] Facial emotion detection
- [ ] Recommendation logic for movies, music, and food

---

*Developed with Python, Streamlit, and modern ML tools.* 