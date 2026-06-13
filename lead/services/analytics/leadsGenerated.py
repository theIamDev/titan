# leads generated as per time range and as per user

from .BaseAnalyticsBuilder import BaseAnalyticsBuilder
from ...models.lead import Lead
from django.db.models import Count
from django.db.models.expressions import RawSQL
from datetime import datetime

# Constant for IST (+5:30 = 330 minutes)
IST_OFFSET_MIN = 330

class leadsGenerated(BaseAnalyticsBuilder):
    def get_initial_queryset(self):
        return Lead.objects.for_user(self.user).order_by('-created_dt', 'id') # type: ignore
        # for testing
        # return Lead.objects.all()

    def apply_annotations(self):
        # Default bucket format
        sql_format = "%%Y-%%m-%%d 00:00:00"

        if self.filterset and 'date' in self.filterset.form.cleaned_data:
            date_value = self.filterset.form.cleaned_data['date']
            
            try:
                start_str, end_str = date_value.split(',')
                start_date = datetime.strptime(start_str, '%Y-%m-%d')
                end_date = datetime.strptime(end_str, '%Y-%m-%d')
                
                delta = end_date - start_date

                if delta.days == 0:
                    sql_format = "%%Y-%%m-%%d %%H:00:00"
                elif delta.days > 90:
                    sql_format = "%%Y-%%m-01 00:00:00"
            except (ValueError, AttributeError):
                pass

        # Apply SQL
        sql = f"DATE_FORMAT(DATE_ADD(created_dt, INTERVAL %s MINUTE), '{sql_format}')"
        
        self.queryset = (
            self.queryset
            .annotate(bucket=RawSQL(sql, (IST_OFFSET_MIN,)))
            .values('bucket')
            .annotate(count=Count('id'))
            .order_by('bucket')
        )
        return self