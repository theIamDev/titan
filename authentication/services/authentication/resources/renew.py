from rest_framework.response import Response
from django.conf import settings
from .tokens import TokenManager
from .cookies import Cookies


def renew_service(request):
    # Get refresh token from HTTP-only cookie
    ACCESS_TOKEN_MAX_AGE = int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds())
    REFRESH_TOKEN = request.COOKIES.get(settings.SIMPLE_JWT["REFRESH_TOKEN_NAME"])
    if not REFRESH_TOKEN:
        return Response({"error": "Refresh token is missing"}, status=403)
    try:
        # Validate refresh token
        token = TokenManager.renew_access_token(REFRESH_TOKEN)
        new_access_token = token.get('access_token')
        response = Response({"access": new_access_token})
        # Set new access token in cookies
        Cookies(response).set_cookie(settings.SIMPLE_JWT["ACCESS_TOKEN_NAME"],new_access_token,ACCESS_TOKEN_MAX_AGE)
        return response
    except Exception as e:
        return Response({"error": "Invalid or expired refresh token"}, status=403)
    
def renew_service_in_body(request):
    refresh_token = request.data.get('refreshToken')
    if not refresh_token:
        return Response({"error": "Refresh token is missing from request body"}, status=400)
    try:
        token = TokenManager.renew_access_token(refresh_token)
        new_access_token = token.get('access_token')
        new_refresh_token = token.get('refresh_token')

        response_data = {
            "accessToken": new_access_token,
            "refreshToken": new_refresh_token
        }
        print('response_data',response_data)
        response = Response(response_data)

        return response

    except Exception as e:
        return Response({"error": "Invalid or expired refresh token"}, status=403)
