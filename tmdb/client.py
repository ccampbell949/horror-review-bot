"""
TMDb client module for accessing movie data from The Movie Database API.

Features:
- Fetch random horror movie details.
- Search for a specific movie and return its overview.
"""

import random
import requests

class TMDBClient:
    BASE_URL = 'https://api.themoviedb.org/3'
    IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'

    def __init__(self, api_key):
        self.api_key = api_key

    def get_random_horror_movie(self):
        page = random.randint(1, 5)
        url = f"{self.BASE_URL}/discover/movie"
        params = {
            "api_key": self.api_key,
            "with_genres": "27",
            "sort_by": "popularity.desc",
            "page": page
        }
        response = requests.get(url, params=params).json()
        results = response.get("results", [])
        if not results:
            return None
        movie = random.choice(results)
        return {
            "title": movie["title"],
            "poster_url": f"{self.IMAGE_BASE_URL}{movie['poster_path']}" if movie.get("poster_path") else None
        }

    def get_movie_overview(self, title):
        url = f"{self.BASE_URL}/search/movie"
        params = {
            "api_key": self.api_key,
            "query": title,
            "include_adult": False
        }
        response = requests.get(url, params=params).json()
        results = response.get("results")
        return results[0].get("overview", "No overview available.") if results else "No overview available."
