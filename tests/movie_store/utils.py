from tests.common.utils import *
from typing import List, Dict, Set, Tuple
from movie_store.models import *
import pytest
from tests.authentication.utils import logged_in_client


MOVIES_URL = "/store/movies/"
GENRES_URL = "/store/genres/"

MOVIE_URL = "/store/movies/{uuid}/"
GENRE_URL = "/store/genres/{uuid}/"


def generate_random_genres(num_genres: int = 10) -> List[Dict]:
    genres = get_unique_random_strings(num_genres, 10)

    genres = [{"title": g} for g in genres]

    return genres


def generate_random_movies(genres: List[Dict], num_movies: int = 10) -> List[Dict]:
    movies = []

    titles = get_unique_random_strings(num_movies, 10)

    for i in range(num_movies):
        title = titles[i]
        description = ""
        director = get_random_string(10)
        year = get_random_int(1970, 2020)
        movie_genres = random.sample(genres, 3)

        movies.append({
            "title": title,
            "description": description,
            "director": director,
            "year": year,
            "genres": movie_genres
        })

    return movies


def create_db_objects(movies: List[Dict], genres: List[Dict]) -> None:
    # TODO: adding keys in place, maybe return?

    genre_objects = {}

    for genre in genres:
        title = genre["title"]
        g = Genre.objects.create(title=title)
        genre_objects[title] = g
        genre["uuid"] = g.uuid

    for movie in movies:
        m = Movie.objects.create(
            title=movie["title"],
            description=movie["description"],
            director=movie["director"],
            year=movie["year"]
        )

        m.genres.set([genre_objects[g["title"]] for g in movie["genres"]])
        movie["uuid"] = m.uuid


def populate_db(num_movies: int = 10, num_genres: int = 5) -> Tuple[List[Dict], List[Dict]]:
    genres = generate_random_genres(num_genres)

    movies = generate_random_movies(genres, num_movies)

    create_db_objects(movies, genres)

    return movies, genres


def movies_equal(m1, m2):
    keys = ["title", "description", "year", "director"]

    m1_genre_set = set([g["title"] for g in m1["genres"]])
    m2_genre_set = set([g["title"] for g in m2["genres"]])

    return dicts_equal(m1, m2, keys) and m1_genre_set == m2_genre_set


def genres_equal(g1, g2):
    return dicts_equal(g1, g2, ["title"])


def dicts_equal(d1: Dict, d2: Dict, keys: List[str] = None) -> bool:
    if keys is None:
        keys = d1.keys()
        keys = keys.union(d2.keys())

    return all([d1[key] == d2[key] for key in keys])
