import os
import random
import requests
from dotenv import load_dotenv
import openai

load_dotenv()  # Load .env file

TMDB_API_KEY = os.getenv('TMDB_API_KEY')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')

if not TMDB_API_KEY:
    print("Error: TMDB_API_KEY not found. Please set it in your .env file.")
    exit(1)

if not OPENROUTER_API_KEY:
    print("Error: OPENROUTER_API_KEY not found. Please set it in your .env file.")
    exit(1)

openai.api_key = OPENROUTER_API_KEY
openai.api_base = "https://openrouter.ai/api/v1"

BASE_URL = 'https://api.themoviedb.org/3'
IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'

def get_random_horror_movie():
    url = f"{BASE_URL}/discover/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "with_genres": "27",  # Horror
        "sort_by": "popularity.desc",
        "page": random.randint(1, 5)
    }
    response = requests.get(url, params=params)
    data = response.json()
    if not data.get("results"):
        print("No movies found.")
        return None
    movie = random.choice(data["results"])
    title = movie["title"]
    poster_path = movie.get("poster_path")
    return {
        "title": title,
        "poster_url": f"{IMAGE_BASE_URL}{poster_path}" if poster_path else "No poster"
    }

def search_movie(movie_name):
    url = f"{BASE_URL}/search/movie"
    params = {
        'api_key': TMDB_API_KEY,
        'query': movie_name,
        'include_adult': False
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data['results']:
        return data['results'][0]
    else:
        print("No results found.")
        return None

from openai import OpenAI

def generate_review_openrouter(movie_title, overview):
    prompt = (
        f"Write a short, eerie, stylish horror movie review in an Instagram style "
        f"for the film '{movie_title}'. Include spooky emojis. "
        f"Here's the overview for context:\n\n{overview}"
    )

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY")
    )

    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1-0528-qwen3-8b:free",  # ✅ Free model
            messages=[
                {"role": "system", "content": "You are a horror movie critic. Write a short and dramatic review of the following film."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.8,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating review: {e}"

if __name__ == "__main__":
    movie = get_random_horror_movie()
    if movie:
        print(f"🎬 {movie['title']}")
        print(f"🖼️ Poster URL: {movie['poster_url']}")
        
        movie_data = search_movie(movie['title'])
        overview = movie_data.get("overview", "No overview provided.")
        review = generate_review_openrouter(movie['title'], overview)
        print(f"\n📝 Review:\n{review}")
