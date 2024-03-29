from django.db import migrations
from movie_store.sample_data import genres, movies


def add_data(apps, schema_editor):
    """
    Adds movies and genres found in movie_store.sample_data to the database
    :param apps:
    :param schema_editor:
    :return: None
    """
    Movie = apps.get_model("movie_store", "Movie")
    Genre = apps.get_model("movie_store", "Genre")

    genre_objects = {}

    for genre in genres:
        obj = Genre.objects.create(title=genre)
        genre_objects[genre] = obj

    for movie in movies:
        movie_genres = [genre_objects[g] for g in movie["genres"]]
        obj = Movie.objects.create(title=movie["title"], description=movie["description"], year=movie["year"],
                                   director=movie["director"])
        obj.genres.set(movie_genres)


class Migration(migrations.Migration):
    dependencies = [
        ('movie_store', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_data),
    ]
