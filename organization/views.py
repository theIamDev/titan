# API core Imports
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from packages.Api_v1.response_v1 import api_out

from .services.locations.getLocation import GetLocation
from .serializers.locationResponseSerializer import LocationResponseSerializer


class Location(APIView):
    def get(self, request):
        user = request.user
        service = GetLocation(user)
        queryset = service.locations_all()
        cleaned_data = LocationResponseSerializer(queryset, many=True).data
        return api_out(success=True,message="data fetched",data=cleaned_data)