import pytest
from tests.authentication.utils import logged_in_client
from tests.movie_store.utils import MOVIES_URL, MOVIE_URL,\
    populate_db, movies_equal
import uuid


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


@pytest.mark.django_db
def test_get_nonexistent_movie(logged_in_client):
    r = logged_in_client.get(MOVIE_URL.format(uuid=uuid.uuid4()))
    assert r.status_code == 404


@pytest.mark.django_db
@pytest.mark.parametrize(
    "field", ["title", "year", "director"]
)
def test_search_movies(logged_in_client, field):
    movies, genres = populate_db(num_movies=100, num_genres=50)

    r = logged_in_client.get(MOVIES_URL)
    assert len(r.data) == len(movies)

    for movie in movies:
        r = logged_in_client.get(MOVIES_URL + "?{}={}".format(field, movie[field]))

        results = r.data
        expected_results = list(filter(lambda m: m[field] == movie[field], movies))

        assert len(r.data) == len(expected_results)

        for result in results:
            assert any([movies_equal(result, m) for m in expected_results])


@pytest.mark.django_db
def test_search_movies_by_genre(logged_in_client):
    movies, genres = populate_db(num_movies=100, num_genres=50)

    r = logged_in_client.get(MOVIES_URL)
    assert len(r.data) == len(movies)

    for genre in genres:
        genre_title = genre["title"]
        r = logged_in_client.get(MOVIES_URL + "?genre={}".format(genre_title))

        results = r.data
        expected_results = list(filter(lambda m: genre_title in [g["title"] for g in m["genres"]], movies))

        assert len(r.data) == len(expected_results)

        for result in results:
            assert any([movies_equal(result, m) for m in expected_results])

