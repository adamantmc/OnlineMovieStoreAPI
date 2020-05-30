import sys, os, django
sys.path.append("~/Desktop/OnlineMoveiStore/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OnlineMovieStore.settings")
django.setup()

from movie_store.models import Movie, Genre
from django.contrib.auth.models import User

User.objects.create_user(username="user1", password="user1")
User.objects.create_user(username="user2", password="user2")

genres = ["Action", "Drama", "Adventure", "Sci-Fi", "Fantasy"]

movies = [
    {
        "title": "Star Wars: Episode IV - A New Hope",
        "description": "Luke Skywalker joins forces with a Jedi Knight, a cocky pilot, a Wookiee and two droids to save the galaxy from the Empire's world-destroying battle station, while also attempting to rescue Princess Leia from the mysterious Darth Vader.",
        "director": "George Lucas",
        "year": 1977,
        "genres": ["Action", "Adventure", "Fantasy"]
    },
    {
        "title": "Star Wars: Episode V - The Empire Strikes Back",
        "description": "After the Rebels are brutally overpowered by the Empire on the ice planet Hoth, Luke Skywalker begins Jedi training with Yoda, while his friends are pursued by Darth Vader and a bounty hunter named Boba Fett all over the galaxy.",
        "director": "George Lucas",
        "year": 1980,
        "genres": ["Action", "Adventure", "Fantasy"]
    },
    {
        "title": "Star Wars: Episode VI - Return of the Jedi",
        "description": "After a daring mission to rescue Han Solo from Jabba the Hutt, the Rebels dispatch to Endor to destroy the second Death Star. Meanwhile, Luke struggles to help Darth Vader back from the dark side without falling into the Emperor's trap.",
        "director": "George Lucas",
        "year": 1983,
        "genres": ["Action", "Adventure", "Fantasy"]
    },
    {
        "title": "Star Wars: Episode VII - The Force Awakens",
        "description": "As a new threat to the galaxy rises, Rey, a desert scavenger, and Finn, an ex-stormtrooper, must join Han Solo and Chewbacca to search for the one hope of restoring peace.",
        "director": "J.J. Abrams",
        "year": "2015",
        "genres": ["Action", "Adventure", "Sci-Fi"]
    },
    {
        "title": "Star Wars: Episode VIII - The Last Jedi",
        "description": "Rey develops her newly discovered abilities with the guidance of Luke Skywalker, who is unsettled by the strength of her powers. Meanwhile, the Resistance prepares for battle with the First Order.",
        "director": "Rian Johnson",
        "year": 2017,
        "genres": ["Action", "Adventure", "Fantasy"]
    },
    {
        "title": "Star Wars: Episode IX - The Rise of Skywalker",
        "description": "The surviving members of the resistance face the First Order once again, and the legendary conflict between the Jedi and the Sith reaches its peak bringing the Skywalker saga to its end.",
        "director": "J.J. Abrams",
        "year": 2019,
        "genres": ["Action", "Adventure", "Sci-Fi"]
    },
    {
        "title": "The Lord of the Rings: The Fellowship of the Ring",
        "description": "A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron.",
        "director": "Peter Jackson",
        "year": 2001,
        "genres": ["Action", "Adventure", "Drama"]
    },
    {
        "title": "The Lord of the Rings: The Two Towers",
        "description": "While Frodo and Sam edge closer to Mordor with the help of the shifty Gollum, the divided fellowship makes a stand against Sauron's new ally, Saruman, and his hordes of Isengard.",
        "director": "Peter Jackson",
        "year": 2002,
        "genres": ["Action", "Adventure", "Drama"]
    },
    {
        "title": "The Lord of the Rings: The Return of the King",
        "description": "Gandalf and Aragorn lead the World of Men against Sauron's army to draw his gaze from Frodo and Sam as they approach Mount Doom with the One Ring.",
        "director": "Peter Jackson",
        "year": 2003,
        "genres": ["Action", "Adventure", "Drama"]
    },
]

genre_objects = {}

for genre in genres:
    obj = Genre.objects.create(title=genre)
    genre_objects[genre] = obj

for movie in movies:
    movie_genres = [genre_objects[g] for g in movie["genres"]]
    obj = Movie.objects.create(title=movie["title"], description=movie["description"], year=movie["year"], director=movie["director"])
    obj.genres.set(movie_genres)