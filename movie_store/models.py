from django.db import models
import uuid
from datetime import datetime
from typing import List, Tuple


def get_valid_years() -> List[Tuple]:
    """
    Get valid years for "year" attribute of Movie model
    :return: list of tuples containing value and human-readable value, same in this case
    """
    start = 1888 # oldest film in existence!
    current_year = datetime.now().year

    return [(x, x) for x in range(start, current_year + 1)]


class Genre(models.Model):
    # primary key automatically added
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.TextField()


class Movie(models.Model):
    # primary key automatically added
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    title = models.TextField()
    description = models.TextField()

    year = models.IntegerField(choices=get_valid_years())
    director = models.TextField()

    genres = models.ManyToManyField(Genre)

