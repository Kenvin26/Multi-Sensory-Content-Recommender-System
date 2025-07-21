import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

data_dir = os.path.join(os.path.dirname(__file__), '../data')
models_dir = os.path.join(os.path.dirname(__file__), '../models')

X = pd.read_csv(os.path.join(data_dir, 'X_encoded.csv'))
y = pd.read_csv(os.path.join(data_dir, 'y_encoded.csv'))

movie_model = RandomForestClassifier(n_estimators=100, random_state=42)
music_model = RandomForestClassifier(n_estimators=100, random_state=42)
food_model = RandomForestClassifier(n_estimators=100, random_state=42)

movie_model.fit(X, y['movie'])
music_model.fit(X, y['music'])
food_model.fit(X, y['food'])

joblib.dump(movie_model, os.path.join(models_dir, 'movie_model.pkl'))
joblib.dump(music_model, os.path.join(models_dir, 'music_model.pkl'))
joblib.dump(food_model, os.path.join(models_dir, 'food_model.pkl'))

print('Models trained and saved successfully.') 