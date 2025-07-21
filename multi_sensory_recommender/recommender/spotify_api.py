import requests
import base64
import time

SPOTIFY_CLIENT_ID = "835915ddbe6642588b410db3402317a9"
SPOTIFY_CLIENT_SECRET = "c864c1ddc9d444078bc1ebc6888db0ca"

_token_info = {"access_token": None, "expires_at": 0}

def get_spotify_token():
    global _token_info
    if _token_info["access_token"] and time.time() < _token_info["expires_at"]:
        return _token_info["access_token"]
    auth_str = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()
    headers = {"Authorization": f"Basic {b64_auth_str}"}
    data = {"grant_type": "client_credentials"}
    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    if response.status_code != 200:
        raise Exception("Failed to authenticate with Spotify API")
    token_data = response.json()
    _token_info["access_token"] = token_data["access_token"]
    _token_info["expires_at"] = time.time() + token_data["expires_in"] - 60
    return _token_info["access_token"]

def get_tracks_by_context(context, max_results=5):
    """
    Fetch tracks from Spotify based on context (emotion, weather, time_of_day).
    Returns a list of track dicts with title, artist, album_art, preview_url, spotify_url, album_name.
    """
    query_terms = [context.get('emotion', ''), context.get('weather', ''), context.get('time_of_day', '')]
    query = " ".join([term for term in query_terms if term])
    if not query:
        query = "happy"  # fallback
    token = get_spotify_token()
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": query, "type": "track", "limit": max_results}
    response = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)
    if response.status_code != 200:
        return []
    data = response.json()
    tracks = []
    for item in data.get("tracks", {}).get("items", []):
        tracks.append({
            "title": item["name"],
            "artist": item["artists"][0]["name"] if item["artists"] else "Unknown",
            "album_art": item["album"]["images"][0]["url"] if item["album"].get("images") else None,
            "preview_url": item.get("preview_url"),
            "spotify_url": item["external_urls"]["spotify"],
            "album_name": item["album"]["name"]
        })
    return tracks 