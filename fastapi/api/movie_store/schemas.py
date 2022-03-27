from movie_store.utils import BaseSchemaConfig
from pydantic import BaseModel, Field
from typing import List
import datetime
import uuid

from movie_store.pagination import create_paginated_response_schema


class Genre(BaseModel):
    uuid: uuid.UUID
    name: str

    class Config:
        orm_mode = True


GenreList = create_paginated_response_schema(Genre)


class Movie(BaseModel):
    uuid: uuid.UUID
    title: str
    description: str
    year: int
    director: str
    genres: List[Genre]

    class Config:
        orm_mode = True


MovieList = create_paginated_response_schema(Movie)


class Rental(BaseModel):
    uuid: uuid.UUID
    movie: Movie = Field(alias="movie_relationship")
    rental_date: datetime.datetime
    return_date: datetime.datetime = None
    fee: float = None

    class Config(BaseSchemaConfig):
        orm_mode = True


RentalList = create_paginated_response_schema(Rental)


class CreateRental(BaseModel):
    movie_uuid: uuid.UUID


class MovieQueryParams(BaseModel):
    search: str = None
    director: str = None
    year: int = None
    genre: str = None
