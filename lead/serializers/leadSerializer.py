from rest_framework import serializers
from ..models.lead import Lead
from .leadPipelineSerializer import StatusResponseSerializer

class LeadDetailSerializer(serializers.ModelSerializer):
    lead_status = StatusResponseSerializer()
    assigned_to_name = serializers.CharField(read_only=True)
    contact = serializers.CharField(source="valid_contact")

    class Meta:
        model = Lead
        fields =  [
            'id',
            'name',
            'email',
            'contact',
            'lead_type',
            'query',
            'recieved_date',
            'interested_in',
            'assigned_to',
            'assigned_to_name',
            'source_assigned',
            'product_code',
            'product_type',
            'follow_up_current_status',
            'source',
            'lead_status',
            'priority',
            'account',
            'organization',
            'location',
            'state',
            'created_by',
            'created_dt',
            'last_updated_by',
            'last_updated_dt',
            'revenue',
            'brokerage',
            'hash_key',
            'golden',
            'sess_id'
        ]

class LeadGetAllResponseSerializer(serializers.ModelSerializer):
    lead_status = StatusResponseSerializer()
    contact = serializers.CharField(source="valid_contact")
    class Meta:
        model = Lead
        fields = [
            'id',
            'name',
            'email',
            'contact',
            'interested_in',
            'source',
            'lead_status',
            'priority',
            'created_dt',
        ]

class LeadResponseSerializer(serializers.ModelSerializer):
    contact = serializers.CharField(source="valid_contact")
    lead_status = StatusResponseSerializer()

    class Meta:
        model = Lead
        fields = [
            'id',
            'name',
            'email',
            'contact',
            'lead_type',
            'query',
            'recieved_date',
            'interested_in',
            'assigned_to',
            'source_assigned',
            'product_code',
            'product_type',
            'follow_up_current_status',
            'source',
            'lead_status',
            'priority',
            'account',
            'organization',
            'location',
            'state',
            'created_by',
            'created_dt',
            'last_updated_by',
            'last_updated_dt',
            'revenue',
            'brokerage',
            'hash_key',
            'golden',
            'sess_id'
        ]

class LeadSearchSerializer(serializers.ModelSerializer):
    contact = serializers.CharField(source="valid_contact")
    class Meta:
        model = Lead
        fields = ['id', 'name', 'email','contact']
