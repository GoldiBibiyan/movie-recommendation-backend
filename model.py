import pandas as pd
import ast
import os
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load datasets
movies = pd.read_csv("tmdb_5000_movies.csv")
credits = pd.read_csv("tmdb_5000_credits.csv")

# Merge datasets
movies = movies.merge(credits, on='title')

# Select important columns
movies = movies[['movie_id', 'title', 'overview',
                 'genres', 'keywords', 'cast', 'crew']]

# Drop null values


movies.dropna(inplace=True)

# Convert stringified JSON columns to list


def convert(text):
    L = []
    for i in ast.literal_eval(text):
        L.append(i['name'])
    return L


movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(
    lambda x: [i['name'] for i in ast.literal_eval(x)[:3]])


def fetch_director(text):
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            return i['name']
    return ''


movies['crew'] = movies['crew'].apply(fetch_director)

# Remove spaces


def collapse(L):
    return [i.replace(" ", "") for i in L]


movies['genres'] = movies['genres'].apply(collapse)
movies['keywords'] = movies['keywords'].apply(collapse)
movies['cast'] = movies['cast'].apply(collapse)

# Create tags column
movies['tags'] = movies['overview'] + " " + \
    movies['genres'].apply(lambda x: " ".join(x)) + " " + \
    movies['keywords'].apply(lambda x: " ".join(x)) + " " + \
    movies['cast'].apply(lambda x: " ".join(x)) + " " + \
    movies['crew']

# Final dataframe
new_df = movies[['movie_id', 'title', 'tags']].copy()

# Force normal Python string type
new_df['title'] = new_df['title'].astype(str)
new_df['tags'] = new_df['tags'].astype(str)

# Vectorization
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()

# Similarity matrix
similarity = cosine_similarity(vectors)
# movies = movies.astype(str)
movies['title'] = movies['title'].astype(str)
os.makedirs('model', exist_ok=True)
# Save files
pickle.dump(new_df.to_dict(), open('model/movie_list.pkl', 'wb'))
pickle.dump(similarity, open('model/similarity.pkl', 'wb'))

print("Model built successfully!")
