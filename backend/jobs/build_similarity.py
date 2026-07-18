import numpy as np
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, DoubleType, StringType
from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, HashingTF, IDF, Normalizer
from pyspark.ml import Pipeline
from delta import configure_spark_with_delta_pip

SILVER_PATH = "delta/silver/movies"
GOLD_PATH = "delta/gold/movie_similarity"


def get_spark():
    builder = (
        SparkSession.builder.appName("MovieRec-Similarity")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        )
    )
    return configure_spark_with_delta_pip(builder).getOrCreate()


def main():
    spark = get_spark()

    silver = spark.read.format("delta").load(SILVER_PATH).fillna({"feature_text": ""})

    # MLlib TF-IDF pipeline
    pipeline = Pipeline(stages=[
        RegexTokenizer(inputCol="feature_text", outputCol="tokens", pattern="\\W"),
        StopWordsRemover(inputCol="tokens", outputCol="filtered"),
        HashingTF(inputCol="filtered", outputCol="tf", numFeatures=5000),
        IDF(inputCol="tf", outputCol="idf_features"),
        Normalizer(inputCol="idf_features", outputCol="features", p=2.0),
    ])

    model = pipeline.fit(silver)
    featured = model.transform(silver).select("movie_id", "features")

    # Collect to driver — dataset is small (~100 movies), safe to do locally
    rows = featured.collect()
    movie_ids = [r["movie_id"] for r in rows]
    vectors = np.array([r["features"].toArray() for r in rows])

    # Cosine similarity: vectors are L2-normalised, so dot product = cosine similarity
    similarity_matrix = vectors @ vectors.T

    schema = StructType([
        StructField("movie_id",              IntegerType(), False),
        StructField("recommended_movie_id",  IntegerType(), False),
        StructField("similarity_score",      DoubleType(),  False),
        StructField("rank",                  IntegerType(), False),
        StructField("model_type",            StringType(),  False),
    ])

    results = []
    for i, movie_id in enumerate(movie_ids):
        scores = sorted(enumerate(similarity_matrix[i]), key=lambda x: x[1], reverse=True)
        for rank, (j, score) in enumerate(scores[1:11], start=1):
            results.append((
                int(movie_id),
                int(movie_ids[j]),
                float(score),
                rank,
                "tfidf_cosine_spark",
            ))

    result_df = spark.createDataFrame(results, schema)
    result_df.write.format("delta").mode("overwrite").save(GOLD_PATH)

    print(f"Built similarity table with {result_df.count()} rows")
    spark.stop()


if __name__ == "__main__":
    main()
