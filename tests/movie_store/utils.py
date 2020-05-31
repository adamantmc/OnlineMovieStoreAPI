from tests.common.utils import *
from typing import List, Dict, Set, Tuple, Iterable
from movie_store.models import *
from movie_store.serializers import RentalSerializer
import datetime
import pytest


MOVIES_URL = "/store/movies/"
GENRES_URL = "/store/genres/"
RENTALS_URL = "/store/rentals/"

MOVIE_URL = "/store/movies/{uuid}/"
GENRE_URL = "/store/genres/{uuid}/"
RENTAL_URL = "/store/rentals/{uuid}/"


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
        movie_genres = random.sample(genres, min(3, len(genres)))

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


def create_rentals(movies: List[Dict], owner, num_rentals: int = 5) -> List[Dict]:
    rentals = []

    assert num_rentals <= len(movies)

    movies_to_rent = random.sample(movies, num_rentals)

    for movie in movies_to_rent:
        rental_date = datetime.datetime.now(datetime.timezone.utc)
        movie_obj = Movie.objects.get(uuid=movie["uuid"])

        r = Rental.objects.create(movie=movie_obj, rental_date=rental_date, owner=owner)

        rentals.append({"movie": str(movie_obj.uuid), "rental_date": rental_date, "uuid": str(r.uuid)})

    return rentals


def movies_equal(m1: dict, m2: dict) -> bool:
    keys = ["title", "description", "year", "director"]

    m1_genre_set = set([g["title"] for g in m1["genres"]])
    m2_genre_set = set([g["title"] for g in m2["genres"]])

    return dicts_equal(m1, m2, keys) and m1_genre_set == m2_genre_set


def genres_equal(g1: dict, g2: dict) -> bool:
    return dicts_equal(g1, g2, ["title"])


def rentals_equal(d1: dict, d2: dict):
    return dicts_equal(d1, d2, ["uuid", "movie"])


def dicts_equal(d1: dict, d2: dict, keys: Iterable = None) -> bool:
    if keys is None:
        keys = set(d1.keys())
        keys = keys.union(set(d2.keys()))

    return all([d1[key] == d2[key] for key in keys])


