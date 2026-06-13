from rest_framework import serializers
from ..models.workflowModels import Stage,Status


class StatusResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ["id", "name"]

class LeadPipelineResponseSerializer(serializers.ModelSerializer):
    # Use the 'related_name' defined in your ForeignKey (related_name="statuses")
    statuses = StatusResponseSerializer(many=True, read_only=True)

    class Meta:
        model = Stage
        fields = ["id","name","statuses"]

