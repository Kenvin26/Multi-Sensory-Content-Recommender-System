import requests

SPOONACULAR_API_KEY = "14ca32cff8404a3ea222e311640f1cbf"


def get_food_by_context(context, max_results=5):
    """
    Fetch recipes from Spoonacular based on context (emotion, weather, time_of_day).
    Returns a list of food dicts with title, image, and source_url.
    """
    query_terms = [context.get('emotion', ''), context.get('weather', ''), context.get('time_of_day', '')]
    query = " ".join([term for term in query_terms if term])
    if not query:
        query = "comfort food"  # fallback
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "apiKey": SPOONACULAR_API_KEY,
        "query": query,
        "number": max_results,
        "addRecipeInformation": True
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return []
    data = response.json()
    foods = []
    for item in data.get("results", []):
        foods.append({
            "title": item.get("title"),
            "image": item.get("image"),
            "source_url": item.get("sourceUrl")
        })
    return foods 