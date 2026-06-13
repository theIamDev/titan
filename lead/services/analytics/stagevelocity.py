from django.db.models import Count, Avg, F, Q, ExpressionWrapper, fields
from django.utils import timezone
from datetime import timedelta
from .BaseAnalyticsBuilder import BaseAnalyticsBuilder
from ...models.lead import Lead

class StageVelocity(BaseAnalyticsBuilder):
    def get_initial_queryset(self):
        return Lead.objects.for_user(self.user) # type: ignore

    def apply_annotations(self):
        """
        Calculates:
        1. Average days spent in current stage.
        2. Stale leads (Leads that haven't moved in > 5 days).
        3. Total volume per stage.
        """
        now = timezone.now()
        stale_threshold = now - timedelta(days=5)
        stats = self.queryset.exclude( # type: ignore
            lead_stage_id=7
        ).values( # type: ignore
            'lead_stage__name'
        ).annotate(
            stage_name=F('lead_stage__name'),
            average_days=Avg(
                ExpressionWrapper(
                    now - F('last_updated_dt'), 
                    output_field=fields.DurationField()
                )
            ),
            total_leads_in_stage=Count('id'),
            stale_lead_count=Count(
                'id', 
                filter=Q(last_updated_dt__lte=stale_threshold)
            )
        ).order_by('lead_stage__order')

        # Clean up the average_days (timedelta to float)
        result = []
        for entry in stats:
            avg_days = entry['average_days']
            result.append({
                "stage_name": entry['stage_name'] or "Unknown",
                "average_days": round(avg_days.total_seconds() / 86400, 1) if avg_days else 0,
                "stale_lead_count": entry['stale_lead_count'],
                "total_leads_in_stage": entry['total_leads_in_stage'],
            })

        self.queryset = result
        return self