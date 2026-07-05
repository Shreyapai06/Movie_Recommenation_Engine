import os
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from deltalake import write_deltalake

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BRONZE_PATH = "delta/bronze/movies"


def fetch_popular_movies(page: int):
    url = "https://api.themoviedb.org/3/movie/popular"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US",
        "page": page
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json()["results"]


def fetch_movie_details(movie_id: int):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        "api_key": TMDB_API_KEY,
        "append_to_response": "credits,keywords"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json()


def main():
    if not TMDB_API_KEY:
        raise ValueError("TMDB_API_KEY not found in environment variables")

    rows = []

    for page in range(1, 6):
        movies = fetch_popular_movies(page)

        for movie in movies:
            movie_id = movie["id"]
            details = fetch_movie_details(movie_id)

            rows.append({
                "movie_id": movie_id,
                "raw_json": str(details),
                "ingested_at": datetime.utcnow().isoformat()
            })

    df = pd.DataFrame(rows)

    write_deltalake(
        BRONZE_PATH,
        df,
        mode="overwrite"
    )

    print(f"Ingested {len(df)} movies into Bronze Delta")


if __name__ == "__main__":
    main()