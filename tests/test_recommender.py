import sys
import os
import pandas as pd
import pytest
from unittest.mock import patch
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import requests
import random
import recommender
from recommender import recommend
from recommender import recommend
from recommender import load_models, movies
import pytest
from unittest.mock import patch
from recommender import recommend, fetch_poster, load_models


# --- External API Integration (TMDB) ---
@patch('recommender.requests.get')
def test_fetch_poster_timeout(mock_get):
    """Integration Test: What if the TMDB API is down or takes too long?"""
    mock_get.side_effect = requests.exceptions.Timeout
    
    result = fetch_poster("Avatar") 
    
    # Assert it returns your specific placeholder image
    assert result == "https://via.placeholder.com/500x750?text=No+Image"

@patch('recommender.requests.get')
def test_fetch_poster_malformed_json(mock_get):
    """Integration Test: What if TMDB returns a 500 error or bad JSON?"""
    mock_get.return_value.json.side_effect = ValueError("Expecting value")
    
    result = fetch_poster("Avatar")
    
    # Assert it returns your specific placeholder image
    assert result == "https://via.placeholder.com/500x750?text=No+Image"

# --- Filesystem Integration ---
@patch('recommender.pickle.load')
def test_load_models_missing_files(mock_pickle_load):
    """Integration Test: What happens if the .pkl files are deleted?"""
    mock_pickle_load.side_effect = FileNotFoundError
    
    # Since your code catches the error, we just call it normally and 
    # assert that it executes without raising the FileNotFoundError
    try:
        load_models()
    except FileNotFoundError:
        pytest.fail("load_models() crashed! It should have caught the FileNotFoundError.")
        
        

# ------------------------------------------------
# Fake Dataset Fixture
# ------------------------------------------------

@pytest.fixture
def fake_data(monkeypatch):
    # Example of what your mock data probably looks like
    data = {
        'movie_id': [1, 2, 3],
        'title': ['Avatar', 'Batman', 'Titanic'],
        'tags': ['action', 'dark', 'romance']
    }
    df = pd.DataFrame(data)
    
    # ADD THIS LINE so the logic in recommender.py has a column to look at
    df['title_search'] = df['title'].str.replace(" ", "").str.strip().str.lower()
    
    # Mock the loading so it uses this data instead of the real .pkl files
    monkeypatch.setattr("recommender.movies", df)
    monkeypatch.setattr("recommender.similarity", np.array([[1, 0.5, 0.2], [0.5, 1, 0.1], [0.2, 0.1, 1]]))
    
    

# ------------------------------------------------
# Core Recommendation Logic Tests
# ------------------------------------------------

@pytest.mark.parametrize(
    "movie",
    ["Avatar", "Batman", "Titanic",]
    
)
def test_valid_movies(fake_data, movie):

    result = recommend(movie)

    assert isinstance(result, list)
    assert len(result) > 0

 


def test_random_valid_movies():

    sample_movies = random.sample(list(recommender.movies["title"]), 30)

    for movie in sample_movies:

        result = recommend(movie)


        assert isinstance(result, list)


def test_movie_not_found(fake_data):

    result = recommend("RandomMovie")

    assert result == {"error": "Movie not found"}


# ------------------------------------------------
# Input Cleaning Tests
# ------------------------------------------------

def test_case_insensitive(fake_data):

    result = recommend("avatar")

    assert isinstance(result, list)


def test_whitespace_input(fake_data):

    result = recommend("  Avatar  ")

    assert isinstance(result, list)


# ------------------------------------------------
# Recommendation Output Tests
# ------------------------------------------------

def test_number_of_recommendations(fake_data):

    result = recommend("Avatar")

    assert len(result) > 1


# ------------------------------------------------
# Poster Fetching Tests (Mocked API)
# ------------------------------------------------

@patch("recommender.requests.get")
def test_fetch_poster_success(mock_get):

    mock_get.return_value.json.return_value = {
        "results": [{"poster_path": "/fake_path.jpg"}]
    }

    poster_url = fetch_poster("Avatar")

    assert poster_url == "https://image.tmdb.org/t/p/w500//fake_path.jpg"


@patch("recommender.requests.get")
def test_fetch_poster_no_image(mock_get):

    mock_get.return_value.json.return_value = {"results": []}

    poster_url = fetch_poster("UnknownMovie123")

    assert poster_url == "https://via.placeholder.com/500x750?text=No+Image"

@pytest.mark.parametrize(
    "movie",
    [
        "Avatar",
        "avatar",
        "AVATAR",
        "  Avatar  ",
        "AvAtAr"
    ],
)
def test_input_variations(fake_data, movie):

    result = recommend(movie)

    assert isinstance(result, list)

    
def test_similarity_order(fake_data):

    result = recommend("Avatar")

    assert isinstance(result, list)

    # Ensure first recommendation is not the same movie
    assert result[0]["title"].lower() != "avatar"


def test_empty_dataset(monkeypatch):

    import recommender

    monkeypatch.setattr(recommender, "movies", None)
    monkeypatch.setattr(recommender, "similarity", None)

    result = recommend("Avatar")
 
    assert isinstance(result, list)
