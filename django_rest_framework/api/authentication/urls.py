from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from authentication.views import logout

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('logout/', logout)
]