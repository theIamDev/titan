
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from packages.authentication.authenticationClass import HeaderJWTAuthentication
from packages.Api_v1.response_v1 import api_out
from packages.Api_v1.pagizon import UniversalPaginator

# API Services 

from .services.ldcntrl.ldcntrlGet import LoadControl
from .serializers.loadControlSerializer import loadControlResponseSerializer
    
class LDCNTRL(APIView):
    authentication_classes = [HeaderJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        service = LoadControl(request.user)
        ldcntrl_data = service.get()
        paged_data = UniversalPaginator(ldcntrl_data,{"page":1,"per_page":10}).get_page()
        serialized_data = loadControlResponseSerializer(paged_data.object_list, many=True)
        cleaned_data = serialized_data.data
        return api_out(success=True,
                       message="fetched",
                       data=cleaned_data
                       )   

