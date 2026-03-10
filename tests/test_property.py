from hypothesis import given, strategies as st, settings
from recommender import recommend

@settings(deadline=None)
@given(st.text())
def test_recommend_never_crashes(movie):

    try:
        recommend(movie)
    except Exception:
        assert False


