# API core Imports
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from packages.authentication.authenticationClass import HeaderJWTAuthentication
from packages.Api_v1.response_v1 import api_out
from packages.Api_v1.pagizon import UniversalPaginator
from rest_framework import status

# service
from ..services.timeline.getTimeline import GetTimelineService

class Timeline_V1(APIView):
    authentication_classes = [HeaderJWTAuthentication]
    permission_classes = [IsAuthenticated]    

    def get(self,request):
        params = request.query_params
        user = request.user
        try:
            service  = GetTimelineService(user,params)
            queryset = service.get_queryset()
            pg = UniversalPaginator(queryset, params)
            page_obj = pg.get_page()
            serialized_data = service.hydrate_timeline_data(user,page_obj.object_list)
            return api_out(
                success=True,message='success',
                data = serialized_data,
                meta={
                    'pagination':pg.get_meta(page_obj)
                }
            )
        except Exception as e:
            return api_out(
                success=False,
                message="An unexpected error occurred.",
                errors={"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )