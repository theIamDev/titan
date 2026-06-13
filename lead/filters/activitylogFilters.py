from django_filters import rest_framework as filters
from ..models import ActivityTimelineLog
from django.utils.dateparse import parse_date
from django.utils.timezone import make_aware
from datetime import datetime, time

class BaseCommaFilter(filters.BaseInFilter, filters.CharFilter):
    """Handles comma-separated strings for __in lookups"""
    pass

class ActivityLogFilter(filters.FilterSet):
    object_identifier = BaseCommaFilter(field_name='object_identifier', lookup_expr='in')
    created_by=BaseCommaFilter(field_name='created_by', lookup_expr='in')
    date = filters.CharFilter(method='filter_by_custom_date')

    class Meta:
        model = ActivityTimelineLog
        fields = ['object_identifier', 'created_by', 'date']

    def filter_by_custom_date(self, queryset, name, value):
        try:
            start_str, end_str = value.split(',')
            # Convert strings to date objects to ensure clean lookups
            start_date = parse_date(start_str)
            end_date = parse_date(end_str)
            if start_date and end_date:
                start_dt = make_aware(datetime.combine(start_date, time.min))
                end_dt = make_aware(datetime.combine(end_date, time.max))
                # queryset = queryset.filter(created_at__date__range=[start_date, end_date])
                queryset = queryset.filter(created_at__range=(start_dt, end_dt))
                return queryset
            
            return queryset
        except (ValueError, AttributeError):
            return queryset
