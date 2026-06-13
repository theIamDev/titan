from django.urls import path
from .views import Location


urlpatterns = [
    # Lead API
    path('location',Location.as_view()),
]





