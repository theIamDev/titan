from rest_framework.views import APIView
from packages.authentication.authenticationClass import HeaderJWTAuthentication
from rest_framework.permissions import IsAuthenticated
from packages.Api_v1.response_v1 import api_out
from packages.Api_v1.pagizon import UniversalPaginator


# services
from .services.users.get.usersGet import UserGetService
from .services.users.create.createUsers import CreateUser

# serializer
from .serializers.getUserListSerializer import GetAllUserSerializer
from .serializers.createUserRequestSerializer import CreateUserSerializer

class User(APIView):
    authentication_classes = [HeaderJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request):
        try:
            user = request.user
            params = request.data
            serializer = CreateUserSerializer(data=params)
            if serializer.is_valid():
                cleaned_params = serializer.validated_data
                service = CreateUser(user,cleaned_params)
                response = service.create()
                return api_out(success=True,message='created',data=response)
            return api_out(success=False,data=[],message='serialization failed')
        except Exception as e:
            return api_out(success=False,data=[],message=str(e))

    def get(self,request):
        user = request.user
        params = request.query_params
        service = UserGetService(user,params)
        user_dataset = service.get_user_list()
        pg =  UniversalPaginator(user_dataset,params,default_per_page=10)
        page_obj = pg.get_page()
        serialized_data = GetAllUserSerializer(page_obj.object_list,many = True)
        data = serialized_data.data
        return api_out(
            success=True,
            message="User list fetched successful",
            data=data,
            meta={
                'pagination':pg.get_meta(page_obj)
            }
        )
    