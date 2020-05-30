from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings as jwt_settings
from rest_framework import permissions


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def logout(request):
    response = Response(status=200)
    response.delete_cookie(jwt_settings.JWT_AUTH_COOKIE)
    return response
