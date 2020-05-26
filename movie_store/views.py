from django.shortcuts import render
from rest_framework import viewsets
from movie_store.models import Movie, Genre
from movie_store.serializers import MovieSerializer, GenreSerializer
from movie_store.filters import ModelAttributeFiltering


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [ModelAttributeFiltering]
    search_fields = ["title", "description", "director", "year"]


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

