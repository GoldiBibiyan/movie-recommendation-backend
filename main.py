from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from recommender import recommend
import os

app = FastAPI()

# Allow your Android app to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Movie Recommendation API"}

@app.get("/recommend/{movie}")
def get_recommendations(movie: str):
    result = recommend(movie)
    return result  # ← was missing this return!
