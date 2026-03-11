import pickle
import requests
import pandas as pd
import os

movies = None
similarity = None
API_KEY = "2cc22bbaf340c85980258d47e3f4aead"
MODEL_DIR = os.environ.get("MODEL_DIR", "model")

def load_models():
    global movies, similarity
    if movies is None:
        movies = pd.DataFrame(pickle.load(open(f'{MODEL_DIR}/movie_list.pkl', 'rb')))
        movies.reset_index(drop=True, inplace=True)
        similarity = pickle.load(open(f'{MODEL_DIR}/similarity.pkl', 'rb'))
        movies['title_search'] = movies['title'].astype(str).str.replace(" ", "").str.strip().str.lower()

def fetch_poster(movie_title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_title}"
    try:
        data = requests.get(url).json()
        if data.get('results'):
            poster_path = data['results'][0].get('poster_path')
            if poster_path:
                return "https://image.tmdb.org/t/p/w500/" + poster_path
    except Exception as e:
        print(f"Error fetching poster: {e}")
    return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(movie):
    load_models()
    movie_search = movie.replace(" ", "").strip().lower()
    if movie_search not in movies['title_search'].values:
        return {"error": "Movie not found"}
    index = movies[movies['title_search'] == movie_search].index[0]
    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )
    results = []
    for i in distances[1:8]:
        movie_title = movies.iloc[i[0]].title
        results.append({
            "title": movie_title,
            "poster": fetch_poster(movie_title)
        })
    return results
