from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, func

from movie_store.db.models import Movie, Genre, Rental
from movie_store import schemas as store_schemas
from movie_store.pagination import PaginationParams

from db.utils import paginate
import uuid

import datetime


def build_movie_filters(movie_query_params: store_schemas.MovieQueryParams):
    alchemy_filters = []
    if movie_query_params.search is not None:
        alchemy_filters.append(
            or_(
                Movie.description.ilike(f"%{movie_query_params.search}%"),
                Movie.title.ilike(f"%{movie_query_params.search}%")
            )
        )
    if movie_query_params.year is not None:
        alchemy_filters.append(Movie.year == movie_query_params.year)
    if movie_query_params.director is not None:
        alchemy_filters.append(Movie.director.ilike(f"%{movie_query_params.director}%"))
    if movie_query_params.genre is not None:
        alchemy_filters.append(Movie.genres.any(Genre.name.ilike(f"%{movie_query_params.genre}%")))

    return alchemy_filters


def get_movies(session: Session, pagination: PaginationParams, movie_query_params: store_schemas.MovieQueryParams):
    query = session.query(Movie).options(joinedload(Movie.genres))

    alchemy_filters = build_movie_filters(movie_query_params=movie_query_params)

    for f in alchemy_filters:
        query = query.filter(f)

    query = paginate(query, page=pagination.page, page_size=pagination.page_size)

    return query.all()


def get_movie(session: Session, movie_uuid: uuid.UUID):
    return session.query(Movie).options(joinedload(Movie.genres)).filter(Movie.uuid == str(movie_uuid)).first()


def count_movies(session: Session) -> int:
    return session.query(func.count(Movie.id)).scalar()


def get_genre(session: Session, genre_uuid: uuid.UUID):
    return session.query(Genre).filter(Genre.uuid == str(genre_uuid)).first()


def get_genres(session: Session, pagination: PaginationParams):
    query = session.query(Genre)
    query = paginate(query, page=pagination.page, page_size=pagination.page_size)
    return query.all()


def count_genres(session: Session) -> int:
    return session.query(func.count(Genre.id)).scalar()


def get_rentals(session: Session, user_id: int, pagination: PaginationParams):
    query = filter_owned_rentals(user_id, session.query(Rental).options(
        joinedload(Rental.movie_relationship), joinedload(Rental.movie_relationship, Movie.genres)
    ))
    query = paginate(query, page=pagination.page, page_size=pagination.page_size)

    return query.all()


def filter_owned_rentals(user_id: int, query):
    return query.filter(Rental.owner == user_id)


def get_rental(session: Session, user_id: int, rental_uuid: uuid.UUID) -> Rental:
    query = filter_owned_rentals(user_id, session.query(Rental))
    query = query.options(
        joinedload(Rental.movie_relationship), joinedload(Rental.movie_relationship, Movie.genres)
    ).filter(Rental.uuid == str(rental_uuid))

    rental = query.first()

    return rental


def get_active_rental_by_movie(session: Session, user_id: int, movie_id: uuid.UUID) -> Rental:
    query = filter_owned_rentals(user_id, session.query(Rental))
    query = query.options(joinedload(Rental.movie_relationship))\
        .filter(Rental.movie == movie_id)\
        .filter(Rental.return_date == None)

    return query.first()


def create_rental(session: Session, user_id: int, movie_id: int) -> Rental:
    r = Rental(owner=user_id, movie=movie_id)

    session.add(r)
    session.commit()

    return get_rental(session, user_id, rental_uuid=r.uuid)


def update_rental(session: Session, rental: Rental, return_date: datetime.datetime, fee: float) -> Rental:
    session.add(rental)

    rental.return_date = return_date
    rental.fee = fee

    session.commit()

    return rental


def count_rentals(session: Session, user_id: int) -> int:
    query = filter_owned_rentals(user_id, session.query(func.count(Rental.id)))
    return query.scalar()
