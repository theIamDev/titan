from rest_framework import serializers
from ..models.locationsModels import Locations

class LocationResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = ["id", "name"]
