from fastapi import APIRouter, HTTPException, Query

from app.services.recommender import (
    get_recommendations_by_movie_id,
    get_recommendations_by_query,
    get_recommendations_by_title,
)

router = APIRouter()


@router.get("/search")
def recommend_by_query(q: str = Query(...)):
    results = get_recommendations_by_query(q)

    if not results:
        raise HTTPException(status_code=404, detail="No recommendations found")

    return {
        "query": q,
        "recommendations": results
    }


@router.get("/{movie_id}")
def recommend_by_movie_id(movie_id: int):
    results = get_recommendations_by_movie_id(movie_id)

    if not results:
        raise HTTPException(status_code=404, detail="No recommendations found")

    return {
        "movie_id": movie_id,
        "recommendations": results
    }


@router.get("/title/{title}")
def recommend_by_title(title: str):
    results = get_recommendations_by_title(title)

    if not results:
        raise HTTPException(status_code=404, detail="No recommendations found")

    return {
        "title": title,
        "recommendations": results
    }