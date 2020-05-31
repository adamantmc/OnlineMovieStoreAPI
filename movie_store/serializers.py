from rest_framework import serializers
from movie_store.models import Movie, Genre, Rental


class CustomSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if hasattr(self, "initial_data"):
            for key in self.initial_data:
                if key not in self.Meta.fields:
                    raise serializers.ValidationError({key: "This field is invalid."})

        return super(CustomSerializer, self).validate(attrs)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ("id", )


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


class RentalUpdateSerializer(CustomSerializer):

    class Meta:
        model = Rental
        fields = ("returned", )


class RentalSerializer(serializers.ModelSerializer):
    movie = serializers.SlugRelatedField(slug_field="uuid", read_only=True)

    class Meta:
        model = Rental
        exclude = ("id", "owner")
