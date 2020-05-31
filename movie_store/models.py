from django.db import models
from django.conf import settings
import uuid
import datetime
from typing import List, Tuple


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

    year = models.IntegerField()
    director = models.TextField()

    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return "{} {} {}".format(self.title, self.director, self.year)


class Rental(models.Model):
    # primary key automatically added
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # Rent owner foreign key
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False, on_delete=models.CASCADE)

    # Rented movie fk
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    # Date of rental
    rental_date = models.DateTimeField(default=get_current_datetime, editable=False)

    # Date of return - filled when the rented movie is returned
    return_date = models.DateTimeField(default=None, editable=False, null=True)

    # Fee - calculated on return
    fee = models.FloatField(default=0, editable=False)

    # Returned - field to PATCH when returning a movie
    returned = models.BooleanField(default=False)
