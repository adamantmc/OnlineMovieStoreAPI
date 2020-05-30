from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from movie_store.models import Movie, Genre, Rental
from movie_store.serializers import MovieSerializer, GenreSerializer, RentalSerializer, RentalCreateSerializer
from movie_store.filters import ModelAttributeFiltering, GenreFiltering
from movie_store.logic.fees import FeeCalculator
from movie_store.permissions import IsOwner, check_permissions
import datetime
import uuid


class MovieViewSet(viewsets.ModelViewSet):
    """
    ViewSet that provides movie listing and detailed movie view
    """
    lookup_field = "uuid"
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    filter_backends = [ModelAttributeFiltering, GenreFiltering]
    search_fields = ["title", "director", "year"]

    permission_classes = [permissions.IsAuthenticated]


class GenreViewSet(viewsets.ModelViewSet):
    """
        ViewSet that provides genre listing and detailed genre view
    """
    lookup_field = "uuid"
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    permission_classes = [permissions.IsAuthenticated]


class RentalViewSet(viewsets.ModelViewSet):
    """
    ViewSet that implements the creation of a Rental, listing current user's rentals
    and getting a rental's details
    """
    lookup_field = "uuid"
    queryset = Rental.objects.all()

    permission_classes = [permissions.IsAuthenticated, IsOwner]
    owner_field = "owner"

    def get_queryset(self):
        if self.action == "list":
            return Rental.objects.filter(owner=self.request.user)

        return Rental.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return RentalCreateSerializer
        else:
            return RentalSerializer

    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)

        valid = serializer.is_valid()

        if not valid:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        movie = serializer.validated_data["movie"]

        non_returned_rentals = self.get_queryset().filter(movie=movie, return_date=None)

        if non_returned_rentals.count() != 0:
            return Response({"error": "This movie is already rented"}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["PATCH"])
@permission_classes([permissions.IsAuthenticated])
def return_movie(request: Request, uuid: uuid.UUID) -> Response:
    """
    View that implements the return of a rented movie
    :param request:
    :param uuid:
    :return:
    """
    rental = get_object_or_404(Rental.objects.all(), uuid=uuid)

    # Function-based views do not support has_object_permissions, so we need to call the
    # check_permissions function defined in the permissions.py files, which is the one that
    # IsOwner uses as well
    if not check_permissions(rental.owner, request.user):
        # Copy django's error
        return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    if rental.return_date is not None:
        return Response({"error": "Movie is already returned"}, status=status.HTTP_400_BAD_REQUEST)

    return_date = datetime.datetime.now(datetime.timezone.utc)
    fee_calculator = FeeCalculator(rental.rental_date, return_date)

    rental.return_date = datetime.datetime.now(datetime.timezone.utc)
    rental.fee = fee_calculator.calculate_fee()
    rental.save()

    serializer = RentalSerializer(rental)

    return Response(serializer.data, status=status.HTTP_200_OK)