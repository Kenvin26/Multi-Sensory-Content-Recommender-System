import requests

TMDB_API_KEY = "3dcfd79acd5d971c4083d2a04e1a3f9b"  # User's TMDB API key
TMDB_BASE_URL = "https://api.themoviedb.org/3"


def get_movies_by_context(context, max_results=5):
    """
    Fetch movies from TMDB based on context (emotion, weather, time_of_day).
    Returns a list of movie dicts with title, overview, and poster_url.
    """
    # Build a query string from context
    query_terms = [context.get('emotion', ''), context.get('weather', ''), context.get('time_of_day', '')]
    query = " ".join([term for term in query_terms if term])
    if not query:
        query = "popular"  # fallback

    search_url = f"{TMDB_BASE_URL}/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": query,
        "language": "en-US",
        "include_adult": False,
        "page": 1
    }
    response = requests.get(search_url, params=params)
    if response.status_code != 200:
        return []
    data = response.json()
    results = data.get("results", [])[:max_results]
    movies = []
    for movie in results:
        movies.append({
            "title": movie.get("title"),
            "overview": movie.get("overview"),
            "poster_url": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get("poster_path") else None
        })
    return movies 