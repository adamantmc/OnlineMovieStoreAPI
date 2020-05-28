from django.urls import include, path
from movie_store.views import MovieViewSet, GenreViewSet, RentalViewSet, return_movie

urlpatterns = [
    path('movies/<uuid:uuid>/', MovieViewSet.as_view({"get": "retrieve"})),
    path('movies/', MovieViewSet.as_view({"get": "list", "post": "create"})),
    path('genres/<uuid:uuid>/', GenreViewSet.as_view({"get": "retrieve"})),
    path('genres/', GenreViewSet.as_view({"get": "list", "post": "create"})),
    path('rental/<uuid:uuid>/return/', return_movie),
    path('rental/<uuid:uuid>/', RentalViewSet.as_view({"get": "retrieve"})),
    path('rental/', RentalViewSet.as_view({"get": "list", "post": "create"}))
]