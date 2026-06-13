# API core Imports
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from packages.authentication.authenticationClass import HeaderJWTAuthentication
from packages.Api_v1.response_v1 import api_out
from packages.Api_v1.pagizon import UniversalPaginator
from rest_framework import status

#services
from ..services.analytics.leadsGenerated import leadsGenerated
from ..services.analytics.stagePipeline import StagePipeline
from ..services.analytics.stagevelocity import StageVelocity
from ..services.analytics.conversionDistribution import ConversionDistribution
from ..services.analytics.homeDashboardKpi import HomeDashboardKpi
from ..services.analytics.teamPerformance import TeamPerformance
from ..services.timeline.getTimeline import GetTimelineService

    
class Base_Analytics_class(APIView):
    authentication_classes = [HeaderJWTAuthentication]
    permission_classes = [IsAuthenticated]
    builder_class = None  # To be defined by child

    def get(self, request):
        user = request.user
        params = request.query_params
        if not self.builder_class:
            raise ValueError("View must define a builder_class")
        builder = self.builder_class(user, params)
        queryset = builder.build()

        return api_out(
            success=True,
            message='',
            data=self.serialize_data(queryset),
            meta={
                "filters_applied": builder.params
            }
        )
    
    def serialize_data(self, queryset):
        # Default: just return values. Child can override for complex JSON.
        return list(queryset.values())
    
class Leads_Generated(Base_Analytics_class):
    builder_class = leadsGenerated

    def serialize_data(self, queryset):
        return queryset

class Stage_Pipeline(Base_Analytics_class):
    builder_class = StagePipeline

    def serialize_data(self, queryset):
        return queryset
    
class Stage_Velocity(Base_Analytics_class):
    builder_class = StageVelocity

    def serialize_data(self, queryset):
        return queryset
    
class Conversion_Distribution(Base_Analytics_class):
    builder_class = ConversionDistribution

    def serialize_data(self, queryset):
        return queryset
    
class Team_Performance(APIView):
    authentication_classes = [HeaderJWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        user = request.user
        params = request.query_params
        result = TeamPerformance(user,params).get()
        return api_out(
            success=True,
            data=result
        )
    
class USER_ACTIONS(APIView):
    authentication_classes = [HeaderJWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        user = request.user
        params = request.query_params
        try:
            service = GetTimelineService(user,params)
            queryset = service.get_queryset()
            filtered_queryset = TeamPerformance.get_user_actions(queryset)
            pg = UniversalPaginator(filtered_queryset, params)
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
    
class Home_Dashboard_Kpi(APIView):
    authentication_classes = [HeaderJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = request.user
        result = HomeDashboardKpi(user).main()
        return api_out(
            success=True,
            data=result
        )
