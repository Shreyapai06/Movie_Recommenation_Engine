import ast
from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import udf, concat, lit, col
from pyspark.sql.types import StringType, DoubleType, IntegerType
from delta import configure_spark_with_delta_pip

BRONZE_PATH = "delta/bronze/movies"
SILVER_PATH = "delta/silver/movies"


def get_spark():
    builder = (
        SparkSession.builder.appName("MovieRec-Transform")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        )
    )
    return configure_spark_with_delta_pip(builder).getOrCreate()


# UDFs to parse nested JSON fields stored as raw strings
@udf(StringType())
def extract_genres(raw):
    try:
        movie = ast.literal_eval(raw)
        return ", ".join(g["name"] for g in movie.get("genres", []))
    except Exception:
        return ""


@udf(StringType())
def extract_cast(raw):
    try:
        movie = ast.literal_eval(raw)
        cast = movie.get("credits", {}).get("cast", [])
        return ", ".join(p["name"] for p in cast[:5])
    except Exception:
        return ""


@udf(StringType())
def extract_director(raw):
    try:
        movie = ast.literal_eval(raw)
        for person in movie.get("credits", {}).get("crew", []):
            if person.get("job") == "Director":
                return person["name"]
    except Exception:
        pass
    return None


@udf(StringType())
def extract_keywords(raw):
    try:
        movie = ast.literal_eval(raw)
        kws = movie.get("keywords", {}).get("keywords", [])
        return ", ".join(k["name"] for k in kws)
    except Exception:
        return ""


@udf(StringType())
def extract_str(raw, field):
    try:
        return str(ast.literal_eval(raw).get(field) or "")
    except Exception:
        return ""


@udf(DoubleType())
def extract_double(raw, field):
    try:
        val = ast.literal_eval(raw).get(field)
        return float(val) if val is not None else None
    except Exception:
        return None


@udf(IntegerType())
def extract_int(raw, field):
    try:
        val = ast.literal_eval(raw).get(field)
        return int(val) if val is not None else None
    except Exception:
        return None


def main():
    spark = get_spark()

    bronze = spark.read.format("delta").load(BRONZE_PATH)

    silver = (
        bronze
        .withColumn("title",        extract_str("raw_json",    lit("title")))
        .withColumn("overview",     extract_str("raw_json",    lit("overview")))
        .withColumn("release_date", extract_str("raw_json",    lit("release_date")))
        .withColumn("poster_path",  extract_str("raw_json",    lit("poster_path")))
        .withColumn("popularity",   extract_double("raw_json", lit("popularity")))
        .withColumn("vote_average", extract_double("raw_json", lit("vote_average")))
        .withColumn("vote_count",   extract_int("raw_json",    lit("vote_count")))
        .withColumn("genres",       extract_genres("raw_json"))
        .withColumn("cast",         extract_cast("raw_json"))
        .withColumn("director",     extract_director("raw_json"))
        .withColumn("keywords",     extract_keywords("raw_json"))
        .withColumn("feature_text", concat(
            lit("Title: "),    col("title"),    lit(" "),
            lit("Overview: "), col("overview"), lit(" "),
            lit("Genres: "),   col("genres"),   lit(" "),
            lit("Cast: "),     col("cast"),     lit(" "),
            lit("Director: "), col("director"), lit(" "),
            lit("Keywords: "), col("keywords"),
        ))
        .drop("raw_json", "ingested_at")
    )

    silver.write.format("delta").mode("overwrite").save(SILVER_PATH)

    print(f"Transformed {silver.count()} movies into Silver Delta")
    spark.stop()


if __name__ == "__main__":
    main()
