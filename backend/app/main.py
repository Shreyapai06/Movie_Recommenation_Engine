from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import movies, recommendations

app = FastAPI(
    title="Movie Recommendation Engine",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(movies.router, prefix="/movies", tags=["Movies"])
app.include_router(recommendations.router, prefix="/recommend", tags=["Recommendations"])


@app.get("/")
def root():
    return {
        "message": "Movie Recommendation API is running"
    }