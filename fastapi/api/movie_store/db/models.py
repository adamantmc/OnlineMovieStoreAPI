from sqlalchemy import String, Integer, Float, Boolean, DateTime, ForeignKey, Column
from sqlalchemy.orm import relationship
from db.conn import Base
import uuid

from movie_store.utils import get_current_datetime


class MovieGenreAssociationTable(Base):
    __tablename__ = "movie_genre_association"

    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(ForeignKey("movie.id"))
    genre_id = Column(ForeignKey("genre.id"))
    

class Movie(Base):
    __tablename__ = "movie"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String, default=lambda: str(uuid.uuid4()), unique=True)

    title = Column(String, unique=True)
    description = Column(String)

    year = Column(Integer)
    director = Column(String)

    genres = relationship('Genre', secondary=MovieGenreAssociationTable.__table__)


class Genre(Base):
    __tablename__ = "genre"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String, default=lambda: str(uuid.uuid4()), unique=True)
    name = Column(String, unique=True)


class Rental(Base):
    __tablename__ = "rental"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String, default=lambda: str(uuid.uuid4()), unique=True)

    # Rent owner foreign key
    owner = Column(ForeignKey("user.id"))

    # Rented movie fk
    movie = Column(ForeignKey("movie.id"))

    # Date of rental
    rental_date = Column(DateTime, default=get_current_datetime)

    # Date of return - filled when the rented movie is returned
    return_date = Column(DateTime, default=None, nullable=True)

    # Fee - calculated on return
    fee = Column(Float, default=0)

    # Returned - field to PATCH when returning a movie
    returned = Column(Boolean, default=False)

    owner_relationship = relationship("User", cascade="delete")
    movie_relationship = relationship("Movie", cascade="delete")
