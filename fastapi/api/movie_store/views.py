from fastapi import APIRouter, HTTPException, Depends, Body

from movie_store.db import queries as store_queries
from movie_store import schemas as store_schemas
from movie_store.logic.fee_calculator import FeeCalculator
from movie_store.pagination import PaginationParams, get_paginated_dict
from movie_store.utils import get_current_datetime

from auth.db import models as auth_models
from auth.authentication import authenticate_user_via_token
import uuid

from db.session import get_session
from sqlalchemy.orm import Session


router = APIRouter(prefix="/store", tags=["store"])


@router.get("/genres/{genre_uuid}/",
            response_model=store_schemas.Genre,
            dependencies=[Depends(authenticate_user_via_token)])
async def retrieve_genre(genre_id: uuid.UUID, session: Session = Depends(get_session)):
    genre = store_queries.get_genre(session, genre_id)

    if genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")

    return genre


@router.get("/genres/", response_model=store_schemas.GenreList, dependencies=[Depends(authenticate_user_via_token)])
async def list_genres(pagination: PaginationParams = Depends(), session: Session = Depends(get_session)):
    genres = store_queries.get_genres(session, pagination)
    total = store_queries.count_genres(session)

    return get_paginated_dict(genres, pagination, total)


@router.get("/movies/{movie_uuid}/",
            response_model=store_schemas.Movie,
            dependencies=[Depends(authenticate_user_via_token)])
async def retrieve_movie(movie_id: uuid.UUID, session: Session = Depends(get_session)):
    movie = store_queries.get_movie(session, movie_id)

    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    return movie


@router.get("/movies/", response_model=store_schemas.MovieList, dependencies=[Depends(authenticate_user_via_token)])
async def list_movies(
        pagination: PaginationParams = Depends(), movie_query_params: store_schemas.MovieQueryParams = Depends(),
        session: Session = Depends(get_session)
):
    movies = store_queries.get_movies(session, pagination=pagination, movie_query_params=movie_query_params)
    total = store_queries.count_movies(session)

    return get_paginated_dict(movies, pagination, total)


@router.get("/rentals/{rental_uuid}/", response_model=store_schemas.Rental, response_model_by_alias=False)
async def retrieve_rental(
        rental_uuid: uuid.UUID, user: auth_models.User = Depends(authenticate_user_via_token),
        session: Session = Depends(get_session)
):
    rental = store_queries.get_rental(session, user.id, rental_uuid)

    if rental is None:
        raise HTTPException(status_code=404, detail="Rental not found")

    return rental


@router.get("/rentals/", response_model=store_schemas.RentalList, response_model_by_alias=False)
async def list_rentals(
    pagination: PaginationParams = Depends(),
    user: auth_models.User = Depends(authenticate_user_via_token),
    session: Session = Depends(get_session)
):
    rentals = store_queries.get_rentals(session, user.id, pagination=pagination)
    total = store_queries.count_rentals(session, user.id)

    return get_paginated_dict(rentals, pagination, total)


@router.post("/rentals/", response_model=store_schemas.Rental, response_model_by_alias=False)
async def create_rental(
    body: store_schemas.CreateRental = Body(...),
    user: auth_models.User = Depends(authenticate_user_via_token),
    session: Session = Depends(get_session)
):
    movie = store_queries.get_movie(session, body.movie_uuid)

    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    previous_rental = store_queries.get_active_rental_by_movie(session, user.id, movie.id)

    if previous_rental is not None:
        raise HTTPException(status_code=400, detail="There is an active rental for that movie")

    rental = store_queries.create_rental(session, user.id, movie.id)

    return rental


@router.patch("/rentals/{rental_uuid}/", response_model=store_schemas.Rental, response_model_by_alias=False)
async def patch_rental(
    rental_uuid: uuid.UUID,
    user: auth_models.User = Depends(authenticate_user_via_token),
    session: Session = Depends(get_session)
):
    rental = store_queries.get_rental(session, user.id, rental_uuid)

    if rental is None:
        raise HTTPException(status_code=404, detail="Rental not found")
    elif rental.return_date is not None:
        raise HTTPException(status_code=400, detail="Rental already returned")

    return_date = get_current_datetime()
    fee_calculator = FeeCalculator(rental.rental_date, return_date)
    fee = fee_calculator.calculate_fee()

    returned_rental = store_queries.update_rental(session, rental, return_date, fee)

    return returned_rental
