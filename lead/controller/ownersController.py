from rest_framework.views import APIView
from packages.Api_v1.response_v1 import api_out
from rest_framework.permissions import IsAuthenticated
from packages.authentication.authenticationClass import HeaderJWTAuthentication

# services 
from ..services.owners.ownerGetService import OwnerGetService

from ..serializers.ownerSerializer import OwnersListResponseSerializer

class Owners(APIView):
    authentication_classes = [HeaderJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        service = OwnerGetService(user)
        user_dataset = service.get_users_list()
        serialized_data = OwnersListResponseSerializer(user_dataset,many = True)
        data = serialized_data.data
        return api_out(
            success=True,
            message="User list fetched successful",
            data=data
        )