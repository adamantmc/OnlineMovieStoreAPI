from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings as jwt_settings
from rest_framework import permissions
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(method="POST",
                     responses={200: "Deletes 'auth' cookie"},
                     operation_summary="Logout",
                     operation_description="Logouts the user by deleting the 'auth' cookie "
                                           "set by the login view")
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def logout(request):
    response = Response(status=200)
    response.delete_cookie(jwt_settings.JWT_AUTH_COOKIE)
    return response
