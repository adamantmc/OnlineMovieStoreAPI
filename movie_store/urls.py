from django.urls import include, path
from movie_store.views import MovieViewSet, GenreViewSet, RentalViewSet

urlpatterns = [
    path('movies/<uuid:uuid>/', MovieViewSet.as_view({"get": "retrieve"})),
    path('movies/', MovieViewSet.as_view({"get": "list"})),
    path('genres/<uuid:uuid>/', GenreViewSet.as_view({"get": "retrieve"})),
    path('genres/', GenreViewSet.as_view({"get": "list"})),
    path('rentals/<uuid:uuid>/', RentalViewSet.as_view({"get": "retrieve", "patch": "update"})),
    path('rentals/', RentalViewSet.as_view({"get": "list", "post": "create"}))
]