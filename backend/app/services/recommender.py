from app.services.delta_reader import read_silver_movies, read_movie_similarity


def get_recommendations_by_movie_id(movie_id: int):
    movies_df = read_silver_movies()
    similarity_df = read_movie_similarity()

    recs = similarity_df[
        similarity_df["movie_id"] == movie_id
    ].sort_values("rank")

    if recs.empty:
        return []

    merged = recs.merge(
        movies_df,
        left_on="recommended_movie_id",
        right_on="movie_id",
        suffixes=("_source", "")
    )

    return merged[
        [
            "recommended_movie_id",
            "title",
            "overview",
            "genres",
            "poster_path",
            "similarity_score",
            "rank"
        ]
    ].to_dict(orient="records")


def get_recommendations_by_title(title: str):
    movies_df = read_silver_movies()

    movie = movies_df[
        movies_df["title"].str.lower() == title.lower()
    ]

    if movie.empty:
        movie = movies_df[
            movies_df["title"].str.contains(title, case=False, na=False)
        ]

    if movie.empty:
        return []

    movie_id = int(movie.iloc[0]["movie_id"])

    return get_recommendations_by_movie_id(movie_id)


def get_recommendations_by_query(query: str):
    title_matches = get_recommendations_by_title(query)

    if title_matches:
        return title_matches

    movies_df = read_silver_movies()

    matches = movies_df[
        movies_df["genres"].str.contains(query, case=False, na=False)
        | movies_df["keywords"].str.contains(query, case=False, na=False)
    ].sort_values("popularity", ascending=False)

    if matches.empty:
        return []

    top_matches = matches.head(10).reset_index(drop=True)

    return [
        {
            "recommended_movie_id": int(row["movie_id"]),
            "title": row["title"],
            "overview": row["overview"],
            "genres": row["genres"],
            "poster_path": row["poster_path"],
            "similarity_score": None,
            "rank": rank
        }
        for rank, row in enumerate(top_matches.to_dict(orient="records"), start=1)
    ]