import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib
import os

data_path = os.path.join(os.path.dirname(__file__), '../data/context_recommendations.csv')
df = pd.read_csv(data_path)

X = df[["weather", "time_of_day", "emotion"]]
y_movie = df["movie"]
y_music = df["music"]
y_food = df["food"]

le_weather = LabelEncoder()
le_time = LabelEncoder()
le_emotion = LabelEncoder()
le_movie = LabelEncoder()
le_music = LabelEncoder()
le_food = LabelEncoder()

X_encoded = X.copy()
X_encoded["weather"] = le_weather.fit_transform(X["weather"])
X_encoded["time_of_day"] = le_time.fit_transform(X["time_of_day"])
X_encoded["emotion"] = le_emotion.fit_transform(X["emotion"])
y_movie_enc = le_movie.fit_transform(y_movie)
y_music_enc = le_music.fit_transform(y_music)
y_food_enc = le_food.fit_transform(y_food)

# Save encoders for later use
os.makedirs(os.path.join(os.path.dirname(__file__), '../models'), exist_ok=True)
joblib.dump(le_weather, os.path.join(os.path.dirname(__file__), '../models/le_weather.pkl'))
joblib.dump(le_time, os.path.join(os.path.dirname(__file__), '../models/le_time.pkl'))
joblib.dump(le_emotion, os.path.join(os.path.dirname(__file__), '../models/le_emotion.pkl'))
joblib.dump(le_movie, os.path.join(os.path.dirname(__file__), '../models/le_movie.pkl'))
joblib.dump(le_music, os.path.join(os.path.dirname(__file__), '../models/le_music.pkl'))
joblib.dump(le_food, os.path.join(os.path.dirname(__file__), '../models/le_food.pkl'))

# Save encoded data for model training
X_encoded.to_csv(os.path.join(os.path.dirname(__file__), '../data/X_encoded.csv'), index=False)
pd.DataFrame({"movie": y_movie_enc, "music": y_music_enc, "food": y_food_enc}).to_csv(os.path.join(os.path.dirname(__file__), '../data/y_encoded.csv'), index=False) 