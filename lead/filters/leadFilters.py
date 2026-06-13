# filters.py
from django_filters import rest_framework as filters
from ..models import Lead
from django.utils.dateparse import parse_date
from django.utils.timezone import make_aware
from datetime import datetime, time

class BaseCommaFilter(filters.BaseInFilter, filters.CharFilter):
    """Handles comma-separated strings for __in lookups"""
    pass

class LeadFilter(filters.FilterSet):
    priority = BaseCommaFilter(field_name='priority', lookup_expr='in')
    status = BaseCommaFilter(field_name='lead_status_id', lookup_expr='in')
    user = BaseCommaFilter(field_name='assigned_to', lookup_expr='in')
    sess_id = BaseCommaFilter(field_name='sess_id', lookup_expr='in')
    
    # Custom method to handle your specific frontend date format: "YYYY-MM-DD,YYYY-MM-DD"
    date = filters.CharFilter(method='filter_by_custom_date')

    class Meta:
        model = Lead
        fields = ['priority', 'status', 'user', 'date','sess_id']

    def filter_by_custom_date(self, queryset, name, value):
        try:
            start_str, end_str = value.split(',')
            start_date = parse_date(start_str)
            end_date = parse_date(end_str)
            if start_date and end_date:
                start_dt = make_aware(datetime.combine(start_date, time.min))
                end_dt = make_aware(datetime.combine(end_date, time.max))
                #return queryset.filter(created_dt__date__range=[start_date, end_date])
                queryset = queryset.filter(created_dt__range=(start_dt, end_dt))
                return queryset
            return queryset
        except (ValueError, AttributeError):
            return queryset