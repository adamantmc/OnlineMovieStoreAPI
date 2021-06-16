from rest_framework import serializers
from movie_store.models import Movie, Genre, Rental


class CustomSerializer(serializers.ModelSerializer):
    """
    Serializer that validates against the read_only_fields attribute of the
    Meta class in order to return a 400 error if a read only field is found
    in the request body.

    Used on creating and updating rentals to return 400 for any non-editable
    fields.
    """
    def validate(self, attrs):
        if hasattr(self, "initial_data"):
            for key in self.initial_data:
                if key in self.Meta.read_only_fields:
                    raise serializers.ValidationError({key: "This field is cannot be modified."})

        return super(CustomSerializer, self).validate(attrs)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ("id", )


class MovieListSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = Movie
        fields = ("uuid", "title", "year", "director", "genres")


class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = Movie
        fields = ("uuid", "title", "year", "description", "director", "genres")


class RentalCreateSerializer(CustomSerializer):
    movie = serializers.SlugRelatedField(slug_field="uuid", queryset=Movie.objects.all())

    class Meta:
        model = Rental
        fields = ("movie", )
        read_only_fields = ("uuid", "owner", "returned", "fee", "rental_date", "return_date")


class RentalUpdateSerializer(CustomSerializer):

    class Meta:
        model = Rental
        fields = ("returned", )
        read_only_fields = ("uuid", "owner", "movie", "fee", "rental_date", "return_date")


class RentalSerializer(serializers.ModelSerializer):
    movie = serializers.SlugRelatedField(slug_field="uuid", read_only=True)

    class Meta:
        model = Rental
        exclude = ("id", "owner")
