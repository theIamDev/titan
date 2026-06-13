from rest_framework import serializers

class OwnersListResponseSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    full_name = serializers.CharField()