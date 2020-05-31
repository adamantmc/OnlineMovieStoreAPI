from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from movie_store.models import Movie, Genre, Rental
from movie_store.serializers import MovieSerializer, GenreSerializer, \
    RentalSerializer, RentalCreateSerializer, RentalUpdateSerializer
from movie_store.filters import ModelAttributeFiltering, GenreFiltering
from movie_store.logic.fees import FeeCalculator
from movie_store.permissions import IsOwner, check_permissions
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
import datetime
import uuid


class Pagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100

    page_size_query_param = 'page_size'
    page_query_param = 'page'


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet that provides movie listing and detailed movie view
    """
    lookup_field = "uuid"
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    filter_backends = [ModelAttributeFiltering, GenreFiltering]
    search_fields = ["title", "director", "year"]

    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination

    @swagger_auto_schema(
        responses={200: MovieSerializer(many=True), 401: "Unauthorized"},
        operation_summary="Movie Listing",
        operation_description="List all movies"
    )
    def list(self, request, *args, **kwargs):
        return super(MovieViewSet, self).list(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={200: MovieSerializer, 401: "Unauthorized", 404: "Not Found."},
        operation_summary="Movie Retrieval",
        operation_description="Retrieve a movie with a GET request to /store/movies/'uuid'/"
    )
    def retrieve(self, request, *args, **kwargs):
        return super(MovieViewSet, self).retrieve(request, *args, **kwargs)


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    """
        ViewSet that provides genre listing and detailed genre view
    """
    lookup_field = "uuid"
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination

    @swagger_auto_schema(
        responses={200: GenreSerializer(many=True), 401: "Unauthorized"},
        operation_summary="Genre Listing",
        operation_description="List all genres"
    )
    def list(self, request, *args, **kwargs):
        return super(GenreViewSet, self).list(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={200: RentalSerializer, 401: "Unauthorized", 404: "Not Found."},
        operation_summary="Genre Retrieval",
        operation_description="Retrieve a genre with a GET request to /store/genres/'uuid'/"
    )
    def retrieve(self, request, *args, **kwargs):
        return super(GenreViewSet, self).retrieve(request, *args, **kwargs)


class RentalViewSet(viewsets.ModelViewSet):
    """
    ViewSet that implements the creation of a Rental, listing current user's rentals,
    getting a rental's details, updating and returning a rental
    """
    lookup_field = "uuid"
    queryset = Rental.objects.all()

    permission_classes = [permissions.IsAuthenticated, IsOwner]
    pagination_class = Pagination
    owner_field = "owner"

    def get_queryset(self):
        if self.action == "list":
            return Rental.objects.filter(owner=self.request.user)

        return Rental.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return RentalCreateSerializer
        elif self.action == "update":
            return RentalUpdateSerializer
        else:
            return RentalSerializer

    @swagger_auto_schema(
        responses={200: RentalSerializer(many=True), 401: "Unauthorized"},
        operation_summary="Rental Listing",
        operation_description="List all user's rentals"
    )
    def list(self, request, *args, **kwargs):
        return super(RentalViewSet, self).list(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={200: RentalSerializer, 401: "Unauthorized", 403: "Forbidden", 404: "Not Found."},
        operation_summary="Rental Retrieval",
        operation_description="Retrieve a rental with a GET request to /store/rentals/'uuid'/"
    )
    def retrieve(self, request, *args, **kwargs):
        return super(RentalViewSet, self).retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={201: RentalSerializer, 400: "Bad Request", 401: "Unauthorized"},
        operation_summary="Rental Creation",
        operation_description="Create a Rental - returns 400_BAD_REQUEST if the same movie is being rent twice "
                              "without being returned first."
    )
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

    @swagger_auto_schema(
        responses={201: RentalSerializer, 400: "Bad Request", 401: "Unauthorized"},
        operation_summary="Rental Update / Return",
        operation_description="Update a Rental - only field that can be updated currently is the 'returned' field. "
                              "When it is set to True, the 'return_date' and 'fee' fields of the Rental are populated. "
                              "PATCHing with returned=True when it already is True (trying to return a movie twice) "
                              "returns a 400_BAD_REQUEST status code."
    )
    def update(self, request, *args, **kwargs):
        # rental object that may be modified
        rental = self.get_object()

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=rental, data=request.data, partial=True)

        valid = serializer.is_valid()
        if not valid:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        # Make sure that the movie can be returned only once
        if "returned" in serializer.validated_data:
            if rental.returned:
                return Response({
                    "error": "The 'returned' field cannot be modified after the movie is returned."
                }, status=status.HTTP_400_BAD_REQUEST)

        # Perform update
        rental = serializer.save()

        # If the "returned" field is set to True on the request body,
        # we must also calculate the fee and the return date and store them
        # in the model instance
        if "returned" in serializer.validated_data and serializer.validated_data["returned"] is True:
            return_date = datetime.datetime.now(datetime.timezone.utc)
            fee_calculator = FeeCalculator(rental.rental_date, return_date)
            fee = fee_calculator.calculate_fee()

            rental.return_date = return_date
            rental.fee = fee
            rental.save()

        # Return the whole object representation
        serializer = RentalSerializer(instance=rental)
        return Response(serializer.data, status=status.HTTP_200_OK)

