import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from delta import configure_spark_with_delta_pip

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BRONZE_PATH = "delta/bronze/movies"


def get_spark():
    builder = (
        SparkSession.builder.appName("MovieRec-Ingest")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        )
    )
    return configure_spark_with_delta_pip(builder).getOrCreate()


def fetch_popular_movies(page: int):
    r = requests.get(
        "https://api.themoviedb.org/3/movie/popular",
        params={"api_key": TMDB_API_KEY, "language": "en-US", "page": page},
    )
    r.raise_for_status()
    return r.json()["results"]


def fetch_movie_details(movie_id: int):
    r = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}",
        params={"api_key": TMDB_API_KEY, "append_to_response": "credits,keywords"},
    )
    r.raise_for_status()
    return r.json()


def main():
    if not TMDB_API_KEY:
        raise ValueError("TMDB_API_KEY not set in environment")

    schema = StructType([
        StructField("movie_id", IntegerType(), False),
        StructField("raw_json", StringType(), False),
        StructField("ingested_at", StringType(), False),
    ])

    rows = []
    for page in range(1, 6):
        for movie in fetch_popular_movies(page):
            details = fetch_movie_details(movie["id"])
            rows.append((movie["id"], str(details), datetime.utcnow().isoformat()))

    spark = get_spark()
    df = spark.createDataFrame(rows, schema)
    df.write.format("delta").mode("overwrite").save(BRONZE_PATH)

    print(f"Ingested {df.count()} movies into Bronze Delta")
    spark.stop()


if __name__ == "__main__":
    main()
