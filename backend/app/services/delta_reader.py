import glob
import pandas as pd

SILVER_MOVIES_PATH = "delta/silver/movies"
GOLD_SIMILARITY_PATH = "delta/gold/movie_similarity"


def read_delta(path: str) -> pd.DataFrame:
    files = sorted(glob.glob(f"{path}/*.parquet"))
    return pd.concat([pd.read_parquet(f) for f in files], ignore_index=True)


def read_silver_movies() -> pd.DataFrame:
    return read_delta(SILVER_MOVIES_PATH).drop_duplicates(subset="movie_id")


def read_movie_similarity() -> pd.DataFrame:
    return read_delta(GOLD_SIMILARITY_PATH)