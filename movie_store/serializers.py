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
        fields = ("uuid", "title", "year", "description", "director", "genres")


# class MovieDetailedSerializer(serializers.ModelSerializer):
#     genres = GenreSerializer(read_only=True, many=True)
#
#     class Meta:
#         model = Movie
#         fields = ("uuid", "title", "description", "year", "director", "genres")
#

class RentalCreateSerializer(serializers.ModelSerializer):
    movie = serializers.SlugRelatedField(slug_field="uuid", queryset=Movie.objects.all())

    def validate(self, attrs):
        if hasattr(self, "initial_data"):
            for key in self.Meta.read_only_fields:
                if key in self.initial_data:
                    raise serializers.ValidationError("Field {} is read-only".format(key))

        return super(RentalCreateSerializer, self).validate(attrs)

    class Meta:
        model = Rental
        exclude = ("id", "owner")
        read_only_fields = ("owner", "rental_date", "return_date", "fee")


class RentalSerializer(serializers.ModelSerializer):
    movie = serializers.SlugRelatedField(slug_field="uuid", read_only=True)

    class Meta:
        model = Rental
        exclude = ("id", "owner")
