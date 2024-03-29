import pytest
from tests.authentication.utils import logged_in_client
from tests.movie_store.utils import GENRES_URL, GENRE_URL,\
    populate_db, genres_equal
from tests.common.utils import get_all_objects_pagination
import uuid


def test_get_genres_no_auth(client):
    r = client.get(GENRES_URL)
    assert r.status_code == 401


@pytest.mark.django_db
def test_get_genre_no_auth(client):
    movies, genres = populate_db(num_movies=10, num_genres=5)

    for genre in genres:
        r = client.get(GENRE_URL.format(uuid=genre["uuid"]))
        assert r.status_code == 401


@pytest.mark.django_db
def test_list_genres(logged_in_client):
    movies, genres = populate_db(num_movies=100, num_genres=50)

    r = logged_in_client.get(GENRES_URL)
    returned_genres = get_all_objects_pagination(logged_in_client, r)

    assert r.data["count"] == len(genres)

    for genre in returned_genres:
        assert any([genres_equal(genre, g) for g in genres])


@pytest.mark.django_db
def test_get_genre(logged_in_client):
    movies, genres = populate_db(num_movies=10, num_genres=5)

    for genre in genres:
        r = logged_in_client.get(GENRE_URL.format(uuid=genre["uuid"]))
        assert genres_equal(genre, r.data)


@pytest.mark.django_db
def test_get_nonexistent_genre(logged_in_client):
    r = logged_in_client.get(GENRE_URL.format(uuid=uuid.uuid4()))
    assert r.status_code == 404
