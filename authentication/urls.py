# from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from authentication.views import Login,Logout,Validate,Renew,Me

urlpatterns = [
    path('auth/api/me', Me.as_view(), name='me'),
    path('auth/api/login', Login.as_view()),
    path('auth/api/logout', Logout.as_view()),
    path('auth/api/validate', Validate.as_view()),
    path('auth/api/token/refresh', Renew.as_view()),
]