# API core Imports
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from packages.authentication.authenticationClass import HeaderJWTAuthentication
from packages.Api_v1.response_v1 import api_out

# services
from ..services.leadPipeline.leadPipelineService import LeadPipelineService

# serializer

from ..serializers.leadPipelineSerializer import LeadPipelineResponseSerializer

class LeadPipeline(APIView):
    authentication_classes = [HeaderJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = request.user
        service = LeadPipelineService(user)
        pipeline_dataset = service.get_pipeline()
        serialized_dataset = LeadPipelineResponseSerializer(pipeline_dataset, many=True)
        cleaned_data = serialized_dataset.data
        return api_out(success=True,
                       message="Lead pipeline was fetched",
                       data=cleaned_data
                       )