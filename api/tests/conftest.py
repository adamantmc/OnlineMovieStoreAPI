import pytest
import pytest_django
from movie_store.models import Movie, Genre

@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        Movie.objects.all().delete()
        Genre.objects.all().delete()