from django.db import models
import uuid
import datetime
from typing import List, Tuple


def get_valid_years() -> List[Tuple]:
    """
    Get valid years for "year" attribute of Movie model
    :return: list of tuples containing value and human-readable value, same in this case
    """
    start = 1888 # oldest film in existence!
    current_year = datetime.datetime.now().year

    return [(x, x) for x in range(start, current_year + 1)]


def get_current_datetime() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


class Genre(models.Model):
    # primary key automatically added
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.TextField(unique=True)

    def __str__(self):
        return self.title


class Movie(models.Model):
    # primary key automatically added
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    title = models.TextField()
    description = models.TextField()

    year = models.IntegerField(choices=get_valid_years())
    director = models.TextField()

    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return "{} {} {}".format(self.title, self.director, self.year)

class Rental(models.Model):
    # primary key automatically added
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # Rented movie fk
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    # Date of rental
    rental_date = models.DateTimeField(default=get_current_datetime, editable=False)

    # Date of return - filled when the rented movie is returned
    return_date = models.DateTimeField(default=None, editable=False, null=True)

    # Fee - calculated on return
    fee = models.FloatField(default=0, editable=False)