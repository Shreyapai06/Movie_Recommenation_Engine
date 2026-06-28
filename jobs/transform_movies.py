import ast
import pandas as pd
from deltalake import DeltaTable, write_deltalake

BRONZE_PATH = "delta/bronze/movies"
SILVER_PATH = "delta/silver/movies"


def extract_director(credits):
    crew = credits.get("crew", [])

    for person in crew:
        if person.get("job") == "Director":
            return person.get("name")

    return None


def extract_cast(credits, limit=5):
    cast = credits.get("cast", [])
    return ", ".join([person.get("name", "") for person in cast[:limit]])


def extract_genres(movie):
    genres = movie.get("genres", [])
    return ", ".join([genre.get("name", "") for genre in genres])


def extract_keywords(movie):
    keywords_data = movie.get("keywords", {})
    keywords = keywords_data.get("keywords", [])
    return ", ".join([keyword.get("name", "") for keyword in keywords])


def main():
    bronze = DeltaTable(BRONZE_PATH).to_pandas()

    rows = []

    for _, row in bronze.iterrows():
        movie = ast.literal_eval(row["raw_json"])

        rows.append({
            "movie_id": movie.get("id"),
            "title": movie.get("title"),
            "overview": movie.get("overview"),
            "genres": extract_genres(movie),
            "cast": extract_cast(movie.get("credits", {})),
            "director": extract_director(movie.get("credits", {})),
            "keywords": extract_keywords(movie),
            "popularity": movie.get("popularity"),
            "vote_average": movie.get("vote_average"),
            "vote_count": movie.get("vote_count"),
            "release_date": movie.get("release_date"),
            "poster_path": movie.get("poster_path")
        })

    df = pd.DataFrame(rows)

    df["feature_text"] = (
        "Title: " + df["title"].fillna("") + " " +
        "Overview: " + df["overview"].fillna("") + " " +
        "Genres: " + df["genres"].fillna("") + " " +
        "Cast: " + df["cast"].fillna("") + " " +
        "Director: " + df["director"].fillna("") + " " +
        "Keywords: " + df["keywords"].fillna("")
    )

    write_deltalake(
        SILVER_PATH,
        df,
        mode="overwrite"
    )

    print(f"Transformed {len(df)} movies into Silver Delta")


if __name__ == "__main__":
    main()