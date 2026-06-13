from rest_framework import serializers
from ..models.subUserAccountModels import sub_users_account

class GetAllUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    user_name = serializers.CharField(source='user.username')
    is_active = serializers.BooleanField(source = 'user.is_active')
    class Meta:
        model = sub_users_account
        fields = ['user_id', 'full_name', 'email','user_name','is_active']