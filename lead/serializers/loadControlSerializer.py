from rest_framework import serializers
from ..models.ldcntrlModel import Ldcntrl


class loadControlResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ldcntrl
        fields = [
            "sess_id",
            "load_type",
            "load_status",
            "source_name",
            "load_timestamp",
            "count"
            ]