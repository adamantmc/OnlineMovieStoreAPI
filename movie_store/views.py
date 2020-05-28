from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from movie_store.models import Movie, Genre, Rental
from movie_store.serializers import MovieSerializer, GenreSerializer, RentalSerializer, RentalCreateSerializer
from movie_store.filters import ModelAttributeFiltering, GenreFiltering
from movie_store.logic import calculate_fee
import datetime
import uuid


class MovieViewSet(viewsets.ModelViewSet):
    lookup_field = "uuid"
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [ModelAttributeFiltering, GenreFiltering]
    search_fields = ["title", "director", "year"]


class GenreViewSet(viewsets.ModelViewSet):
    lookup_field = "uuid"
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class RentalViewSet(viewsets.ModelViewSet):
    lookup_field = "uuid"
    queryset = Rental.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return RentalCreateSerializer
        else:
            return RentalSerializer


@api_view(["PATCH"])
def return_movie(request: Request, uuid: uuid.UUID) -> Response:
    rental = get_object_or_404(Rental.objects.all(), uuid=uuid)

    if rental.return_date is not None:
        return Response({"error": "Movie is already returned"}, status=status.HTTP_400_BAD_REQUEST)

    rental.return_date = datetime.datetime.now(datetime.timezone.utc)
    rental.fee = calculate_fee(rental.rental_date, rental.return_date)
    rental.save()

    serializer = RentalSerializer(rental)

    return Response(serializer.data, status=status.HTTP_200_OK)