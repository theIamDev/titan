from rest_framework.views import APIView
from packages.authentication.authenticationClass import HeaderJWTAuthentication

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from packages.Api_v1.response_v1 import api_out

# services
from .services.authentication.auth import Authentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny

class Me(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = request.user
        user_data = Authentication().me(user)
        if user_data:
            return api_out(success=True,message="successfully user fetch",data=user_data)
        else:
            return api_out(success=False,message="unsuccessfully user fetch",data={})

class Login(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        return Authentication().login(request)


class Renew(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        print('request',request.data)
        return Authentication().renew(request)

class Logout(APIView):
    authentication_classes = [HeaderJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return Authentication().logout(request)

class Validate(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        print('called')
        print(request)
        print(request.headers)
        return Authentication().validate(request)