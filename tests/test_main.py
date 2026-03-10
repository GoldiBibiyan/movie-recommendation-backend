from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app
import pytest
from recommender import recommend
from recommender import load_models, movies
client = TestClient(app)



# ------------------------------------------------
# 1. Basic API Success / Error
# ------------------------------------------------

def test_recommend_movie_endpoint():
    response = client.get("/recommend/avatar")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert 4 <= len(data) <= 9


def test_recommend_movie_not_found():
    response = client.get("/recommend/thismoviedoesnotexist")

    assert response.status_code == 200
    assert response.json() == {"error": "Movie not found"}


# ------------------------------------------------
# 2. Input Sanitization
# ------------------------------------------------

def test_case_and_space_insensitivity():
    response = client.get("/recommend/   bAtMaN   ")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


# ------------------------------------------------
# 3. Routing / Path Validation
# ------------------------------------------------

def test_missing_movie_parameter():
    response = client.get("/recommend/")

    assert response.status_code == 404


# ------------------------------------------------
# 4. Response Schema
# ------------------------------------------------

def test_response_schema():
    response = client.get("/recommend/spectre")

    data = response.json()

    for item in data:
        assert "title" in item
        assert "poster" in item
        assert isinstance(item["title"], str)
        assert isinstance(item["poster"], str)


def test_response_content_type():
    response = client.get("/recommend/avatar")

    assert response.headers["content-type"] == "application/json"


# ------------------------------------------------
# 5. Edge Case Inputs
# ------------------------------------------------

def test_special_character_movie():
    response = client.get("/recommend/Avatar%20(2009)")

    assert response.status_code == 200


def test_very_long_movie_name():
    long_string = "a" * 500

    response = client.get(f"/recommend/{long_string}")

    assert response.status_code == 200


# ------------------------------------------------
# 6. Stability / Multiple Requests
# ------------------------------------------------

def test_multiple_requests():
    for _ in range(10):
        response = client.get("/recommend/avatar")
        assert response.status_code == 200


@pytest.mark.parametrize(
    "movie",
    [
        "Avatar",
        "Titanic",
        "Avengers",
        "Batman",
        "Superman",
        "Inception",
        "Iron Man"
    ]
)
def test_multiple_movie_queries(client, movie):

    response = client.get(f"/recommend/{movie}")

    assert response.status_code == 200


#Test API stability
def test_api_stress(client):

    for _ in range(20):

        response = client.get("/recommend/avatar")

        assert response.status_code == 200
        
def test_system_multiple_requests_state():
    """System Test: Does the backend maintain correct state across multiple rapid calls?"""
    response1 = client.get("/recommend/avatar")
    response2 = client.get("/recommend/spectre")
    response3 = client.get("/recommend/batman")
    
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response3.status_code == 200
    # Ensure it doesn't return the same cached results for different movies
    assert response1.json() != response2.json()
    

@pytest.mark.parametrize(
    "movie",
    [
        "%%%%%",
        "!!!",
        "###",
        "@@@"
    ]
)
def test_special_character_inputs(client, movie):

    response = client.get(f"/recommend/{movie}")

    assert response.status_code in [200, 404]
