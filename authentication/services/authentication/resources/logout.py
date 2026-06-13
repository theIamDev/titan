from django.http import JsonResponse
from rest_framework import status
from ..resources.cookies import Cookies
from django.conf import settings

def logout_service():
    ACCESS_TOKEN_NAME = settings.SIMPLE_JWT["ACCESS_TOKEN_NAME"]
    REFRESH_TOKEN_NAME = settings.SIMPLE_JWT["REFRESH_TOKEN_NAME"]
    response = JsonResponse({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    Cookies(response).delete_cookie(ACCESS_TOKEN_NAME)
    Cookies(response).delete_cookie(REFRESH_TOKEN_NAME)
    return response