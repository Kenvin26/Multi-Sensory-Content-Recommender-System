import joblib
import os
import numpy as np
from .tmdb_api import get_movies_by_context
from .spotify_api import get_tracks_by_context
from .food_api import get_food_by_context

dir_path = os.path.dirname(__file__)
models_dir = os.path.join(dir_path, '../models')

# Load models
movie_model = joblib.load(os.path.join(models_dir, 'movie_model.pkl'))
music_model = joblib.load(os.path.join(models_dir, 'music_model.pkl'))
food_model = joblib.load(os.path.join(models_dir, 'food_model.pkl'))

# Load encoders
le_weather = joblib.load(os.path.join(models_dir, 'le_weather.pkl'))
le_time = joblib.load(os.path.join(models_dir, 'le_time.pkl'))
le_emotion = joblib.load(os.path.join(models_dir, 'le_emotion.pkl'))
le_movie = joblib.load(os.path.join(models_dir, 'le_movie.pkl'))
le_music = joblib.load(os.path.join(models_dir, 'le_music.pkl'))
le_food = joblib.load(os.path.join(models_dir, 'le_food.pkl'))

def predict_ml(context):
    # Normalize emotion input
    emotion = context["emotion"].strip().lower()
    print("Emotion received:", emotion)
    print("Known classes:", le_emotion.classes_)
    x = np.array([
        le_weather.transform([context["weather"]])[0],
        le_time.transform([context["time_of_day"]])[0],
        le_emotion.transform([emotion])[0]
    ]).reshape(1, -1)
    # Use TMDB for movie recommendations
    movie_pred = get_movies_by_context(context)
    # Use Spotify for music recommendations
    music_pred = get_tracks_by_context(context)
    # Use Spoonacular for food recommendations
    food_pred = get_food_by_context(context)
    return {
        "movie": movie_pred,
        "music": music_pred,
        "food": food_pred
    } 