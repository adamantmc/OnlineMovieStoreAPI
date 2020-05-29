import pytest
from tests.authentication.utils import logged_in_client
from tests.movie_store.utils import MOVIES_URL, MOVIE_URL,\
    populate_db, movies_equal


def test_get_movies_no_auth(client):
    r = client.get(MOVIES_URL)
    assert r.status_code == 401


@pytest.mark.django_db
def test_get_movie_no_auth(client):
    movies, genres = populate_db(num_movies=10, num_genres=5)

    for movie in movies:
        r = client.get(MOVIE_URL.format(uuid=movie["uuid"]))
        assert r.status_code == 401


@pytest.mark.django_db
def test_list_movies(logged_in_client):
    movies, genres = populate_db(num_movies=100, num_genres=50)

    r = logged_in_client.get(MOVIES_URL)
    returned_movies = r.data

    assert len(r.data) == len(movies)

    for movie in returned_movies:
        assert any([movies_equal(movie, m) for m in movies])


@pytest.mark.django_db
def test_get_movie(logged_in_client):
    movies, genres = populate_db(num_movies=10, num_genres=5)

    for movie in movies:
        r = logged_in_client.get(MOVIE_URL.format(uuid=movie["uuid"]))
        assert movies_equal(movie, r.data)