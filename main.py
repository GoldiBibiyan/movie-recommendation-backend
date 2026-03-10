'''from fastapi import FastAPI

from recommender import recommend

app = FastAPI()

@app.get("/recommend/{movie}")
def recommend_movie(movie: str):
    return recommend(movie)'''


from fastapi import FastAPI
from recommender import recommend

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Movie Recommendation API"}

@app.get("/recommend/{movie}")
def get_recommendations(movie: str):
    result = recommend(movie)
    return {"recommendations": result}
