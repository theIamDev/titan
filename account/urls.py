from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from .views import User

urlpatterns = [ 
    path('', User.as_view(), name='User'), 
    path('create', User.as_view(), name='CreateUser'), 
]