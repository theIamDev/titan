from .resources.login import login_service
from .resources.logout import logout_service
from .resources.validate import validate_service
from .resources.renew import renew_service_in_body #renew_service
from .resources.me import fetch_user
from django.http import JsonResponse

class Authentication():
    def me(self,user):
        return fetch_user(user)

    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if username is None or password is None:
            return JsonResponse({'message': 'Error: username or password not provided in the request.'}, status=401)
        return login_service(username, password)

    def renew(self,request):
        return renew_service_in_body(request)
        #return renew_service(request)

    def logout(self,request):
        return logout_service()
    
    def validate(self,request):
        return validate_service()
