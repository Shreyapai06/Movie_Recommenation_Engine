import pandas as pd
import numpy as np
from deltalake import DeltaTable, write_deltalake
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SILVER_PATH = "delta/silver/movies"
GOLD_PATH = "delta/gold/movie_similarity"


def main():
    df = DeltaTable(SILVER_PATH).to_pandas()

    df["feature_text"] = df["feature_text"].fillna("")

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=5000
    )

    vectors = vectorizer.fit_transform(df["feature_text"])
    similarity_matrix = cosine_similarity(vectors)

    results = []

    for idx, movie in df.iterrows():
        scores = list(enumerate(similarity_matrix[idx]))

        scores = sorted(
            scores,
            key=lambda x: x[1],
            reverse=True
        )

        top_scores = scores[1:11]

        for rank, item in enumerate(top_scores, start=1):
            rec_idx, score = item

            results.append({
                "movie_id": int(movie["movie_id"]),
                "recommended_movie_id": int(df.iloc[rec_idx]["movie_id"]),
                "similarity_score": float(score),
                "rank": rank,
                "model_type": "tfidf_cosine"
            })

    result_df = pd.DataFrame(results)

    write_deltalake(
        GOLD_PATH,
        result_df,
        mode="overwrite"
    )

    print(f"Built similarity table with {len(result_df)} rows")


if __name__ == "__main__":
    main()