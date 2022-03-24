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

from movie_store.db.models import Movie, Genre, Rental, MovieGenreAssociationTable
from auth.db.models import User

from db.conn import Session, engine


def create_tables():
    Genre.__table__.drop(engine)
    Movie.__table__.drop(engine)
    Rental.__table__.drop(engine)
    MovieGenreAssociationTable.__table__.drop(engine)
    User.__table__.drop(engine)

    Genre.__table__.create(engine)
    Movie.__table__.create(engine)
    Rental.__table__.create(engine)
    MovieGenreAssociationTable.__table__.create(engine)
    User.__table__.create(engine)


def add_data():
    genre_objects = {}
    movie_objects_by_genre = {}

    with Session() as session: 
        for genre in genres:
            g = Genre(name=genre)
            session.add(g)
            genre_objects[genre] = g
        
        session.flush()

        for movie in movies:
            m = Movie(title=movie["title"], description=movie["description"], director=movie["director"], year=movie["year"])
            session.add(m)
            for genre in movie["genres"]:
                if genre not in movie_objects_by_genre:
                    movie_objects_by_genre[genre] = []
                
                movie_objects_by_genre[genre].append(m)

        session.flush()

        for genre in genre_objects.values():
            for movie in movie_objects_by_genre[genre.name]:
                mga = MovieGenreAssociationTable(movie_id=movie.id, genre_id=genre.id)
                session.add(mga)
        
        session.commit()


if __name__ == "__main__":
    create_tables()
    add_data()
