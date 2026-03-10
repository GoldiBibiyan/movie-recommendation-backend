from recommender import load_models
'''
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))'''
import recommender
import pytest
import ast

# Assuming you separate your helper functions into a recognizable scope, 
# or just import them directly if they are globally defined in model.py
from model import convert, fetch_director, collapse 

# --- Unit Tests for convert() ---
@pytest.mark.parametrize("input_text, expected_output", [
    ('[{"name": "Action"}, {"name": "Sci-Fi"}]', ['Action', 'Sci-Fi']),
    ('[{"name": "Drama"}]', ['Drama']),
    ('[]', []), # Edge case: Empty list
])
def test_convert(input_text, expected_output):
    assert convert(input_text) == expected_output

# --- Unit Tests for fetch_director() ---
@pytest.mark.parametrize("input_text, expected_director", [
    ('[{"job": "Director", "name": "Christopher Nolan"}, {"job": "Writer", "name": "Jonathan"}]', 'Christopher Nolan'),
    ('[{"job": "Producer", "name": "Kevin Feige"}]', ''), # Edge case: No director
    ('[]', ''), # Edge case: Empty crew
])
def test_fetch_director(input_text, expected_director):
    assert fetch_director(input_text) == expected_director

# --- Unit Tests for collapse() ---
@pytest.mark.parametrize("input_list, expected_output", [
    (['Science Fiction', 'Action'], ['ScienceFiction', 'Action']),
    (['Tom Holland', 'Zendaya'], ['TomHolland', 'Zendaya']),
    (['NoSpacesHere'], ['NoSpacesHere']),
    ([], []), # Edge case: Empty list
    (['   '], ['']), # Edge case: Just spaces
])
def test_collapse(input_list, expected_output):
    assert collapse(input_list) == expected_output
    
    


def test_model_loading_state():

    load_models()

    assert recommender.movies is not None
    assert recommender.similarity is not None
 
    assert "title_search" in recommender.movies.columns



def test_similarity_matrix_shape():

    sim = recommender.similarity

    assert len(sim) == len(recommender.movies)



def test_movies_dataframe_columns():

    df = recommender.movies

    assert "title" in df.columns
    assert "title_search" in df.columns
