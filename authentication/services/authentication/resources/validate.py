from django.http import JsonResponse
from rest_framework import status

def validate_service():
    return JsonResponse({'message': 'Validated'}, status=status.HTTP_200_OK)