from rest_framework import serializers
from django.contrib.auth.models import User

class CreateUserSerializer(serializers.Serializer):
    # Auth User Fields
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    
    # Profile Fields
    middle_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    mobile = serializers.CharField(max_length=15, required=False, allow_blank=True)
    
    # Foreign Key IDs (received as strings/integers from params)
    supervisor_id = serializers.IntegerField()
    role_id = serializers.IntegerField()
    location_id = serializers.IntegerField(required=False)

    def validate_email(self, value):
        """Check if user already exists."""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value