from rest_framework import serializers
from movie_store.models import Movie, Genre, Rental


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ("id", )


class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = Movie
        fields = ("uuid", "title", "description", "year", "director", "genres")


class RentalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        exclude = ("id", )


class RentalSerializer(serializers.ModelSerializer):
    movie = serializers.SlugRelatedField(slug_field="uuid", read_only=True)

    class Meta:
        model = Rental
        exclude = ("id", )