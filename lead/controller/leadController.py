from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from packages.authentication.authenticationClass import HeaderJWTAuthentication
from rest_framework import status
from packages.Api_v1.response_v1 import api_out
from packages.Api_v1.pagizon import UniversalPaginator
from django.http import StreamingHttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test

# service layer
from ..services.lead.search_lead_service import search_lead
from ..services.lead.updateLead import lead_update
from ..services.lead.leadAction import lead_action
from ..services.lead.create.createController import LeadCreationController
from ..services.lead.get.leadGet import LeadGetService
from ..services.lead.get.LeadDetailsGet import LeadDetailService
from ..services.lead.leadExport import LeadExportService

# serializers
from ..serializers.leadSerializer import LeadSearchSerializer,LeadDetailSerializer,LeadGetAllResponseSerializer
    
class LeadList(APIView):
    authentication_classes = [HeaderJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        params = request.query_params
        try:
            service = LeadGetService(user, params)
            queryset = service.get()
            pg = UniversalPaginator(queryset, params)
            page_obj = pg.get_page()
            serializer = LeadGetAllResponseSerializer(page_obj.object_list, many=True)
            return api_out(
                success=True,
                message='Success',
                data=serializer.data,
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

    def put(self, request):
        data = request.data
        user = request.user
        res = lead_update(user,data)
        if res.get('success',False):
            return api_out(success=True,message=res.get('msg',"Successful"))
        else:
            return api_out(success=False,message=res.get('msg',"Failed"),status=status.HTTP_400_BAD_REQUEST)
    
    def post(self,request):
        data = request.data
        user = request.user
        success, message, lead_id, count, session_id = LeadCreationController(user,data).create() # type: ignore
        num = count
        if lead_id:
            num = lead_id
        if success:
            return api_out(success=True,message=str(message),data=num,meta={"session_id":session_id})
        else:
            return api_out(success=False,message=str(message),status=status.HTTP_400_BAD_REQUEST)

class LeadDetail(APIView):
    authentication_classes = [HeaderJWTAuthentication]
    permission_classes = [IsAuthenticated]  

    def get(self,request, id):
        user = request.user
        service = LeadDetailService(user=user, lead_id=id)
        data = service.get()
        if not data:
            return api_out(
                success=False, 
                message="Lead not found or access restricted", 
                data=None,
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = LeadDetailSerializer(data)
        final_data = service.enrich_data(serializer.data) # type: ignore
        return api_out(success=True,message="",data=final_data)

class SearchLead(APIView):
    authentication_classes = [HeaderJWTAuthentication]
    permission_classes = [IsAuthenticated]  

    def get(self,request):
        search = request.query_params.get("s", "").strip()
        data,keyword = search_lead(search,request.user)
        serializedData = LeadSearchSerializer(data,many=True).data
        return api_out(
            success=True,
            message="Lead search successful.",
            data=serializedData,
            status=status.HTTP_200_OK,
            meta={"keyword":keyword}
        )
    

class Export(APIView):
    authentication_classes = [HeaderJWTAuthentication]
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        service = LeadExportService(user=request.user, params=request.query_params)
        filename = service.get_file_name()
        response = StreamingHttpResponse(
            service.stream_csv(),
            content_type="text/csv"
        )
        response['Content-Disposition'] = 'attachment; filename='+filename
        # Explicitly allow this header if using CORS
        response['Access-Control-Expose-Headers'] = 'Content-Disposition'
        
        return response
    
class LeadActions(APIView):
    authentication_classes = [HeaderJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self,request):
        data = request.data
        user = request.user
        res = lead_action(user,data)
        if res['success']:
            return api_out(success=True,message=res['msg'])
        else:
            return api_out(success=False,message=res['msg'],status=status.HTTP_400_BAD_REQUEST)
        