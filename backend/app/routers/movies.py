import numpy as np
from fastapi import APIRouter, Query, HTTPException
from app.services.delta_reader import read_silver_movies

router = APIRouter()


@router.get("/")
def get_movies():
    df = read_silver_movies()
    return df.replace({np.nan: None}).to_dict(orient="records")

@router.get("/search")
def search_movies(query: str = Query(...)):
    df = read_silver_movies()

    results = df[
        df["title"].str.contains(query, case=False, na=False)
    ]

    return results.head(10).to_dict(orient="records")


@router.get("/{movie_id}")
def get_movie(movie_id: int):
    df = read_silver_movies()

    movie = df[df["movie_id"] == movie_id]

    if movie.empty:
        raise HTTPException(status_code=404, detail="Movie not found")

    return movie.replace({np.nan: None}).iloc[0].to_dict()