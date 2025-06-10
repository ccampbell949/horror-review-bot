import os
import random
import requests
from dotenv import load_dotenv

load_dotenv()  # Load .env file

API_KEY = os.getenv('TMDB_API_KEY')
if not API_KEY:
    print("Error: TMDB_API_KEY not found. Please set it in your .env file.")
    exit(1)

BASE_URL = 'https://api.themoviedb.org/3'
IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'  # w500 is the poster size

def get_random_horror_movie():
    url = f"{BASE_URL}/discover/movie"
    params = {
        "api_key": API_KEY,
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

if __name__ == "__main__":
    movie = get_random_horror_movie()
    if movie:
        print(f"🎬 {movie['title']}")
        print(f"🖼️ Poster URL: {movie['poster_url']}")
