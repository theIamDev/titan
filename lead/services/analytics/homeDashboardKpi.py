from django.db.models import Q, Count, IntegerField
from django.db.models.functions import Cast
from django.utils import timezone
from datetime import timedelta
from ...models.lead import Lead
from ...models.ActivityTimelineLogModel import ActivityTimelineLog

# Refactored for Readability and Performance
class HomeDashboardKpi:
    def __init__(self, user):
        self.user = user
        self.kpi = {}
        
        # Move configuration to a class-level Mapping or Enum for maintainability
        self.STAGES = {
            'ACTIONABLE': [1, 2, 3, 4, 5],
            'FRESH': [1],
            'QUALIFIED': 3,
            'ENGAGEMENT': 4,
        }
        self.STATUS = {
            'WON': 13,
            'LOST': 14,
            'SPAM': 15
        }

    def get_initial_queryset(self):
        """Initial filter with select_related if necessary."""
        return Lead.objects.for_user(self.user).filter( # type: ignore
            state='active', 
            assigned_to=self.user.id
        ).exclude(lead_status_id=self.STATUS['SPAM'])

    def main(self):
        data = self.apply_computation()
        return self.apply_post_filter(data)

    def apply_computation(self):
        now = timezone.now()
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Improvement: Filter Activity logs first to reduce the join set
        # instead of a correlated subquery inside the annotation.
        touched_lead_ids = ActivityTimelineLog.objects.for_user(self.user).filter( # type: ignore
            created_at__gte=start_of_day,
            created_at__lte=now
        ).exclude(
            activity_type='Lead Creation'
        ).values_list('object_identifier', flat=True).distinct()

        # Single optimized aggregation
        metrics = self.get_initial_queryset().aggregate(
            actionable_leads=Count('id', filter=Q(lead_stage_id__in=self.STAGES['ACTIONABLE'])),
            new_leads_ready=Count('id', filter=Q(lead_stage_id__in=self.STAGES['FRESH'])),
            
            # Use the pre-fetched list for a simple IN lookup (Faster for daily batches)
            touched_leads_today=Count('id', filter=Q(id__in=touched_lead_ids)),
            
            qualified_leads_today=Count('id', filter=Q(
                lead_stage_id=self.STAGES['QUALIFIED'], 
                last_updated_dt__gte=start_of_day
            )),
            engagement_leads_today=Count('id', filter=Q(
                lead_stage_id=self.STAGES['ENGAGEMENT'], 
                last_updated_dt__gte=start_of_day
            )),
            won_today=Count('id', filter=Q(
                lead_status_id=self.STATUS['WON'], 
                last_updated_dt__gte=start_of_day
            )),
            lost_today=Count('id', filter=Q(
                lead_status_id=self.STATUS['LOST'], 
                last_updated_dt__gte=start_of_day
            )),
        )
        return metrics

    def apply_post_filter(self, d):
        def get_pct(num, den):
            return round((num / den) * 100, 2) if den > 0 else 0

        total_decided = d['won_today'] + d['lost_today']
        
        return {
            **d,
            'daily_contact_to_qualified_pct': get_pct(d['qualified_leads_today'], d['touched_leads_today']),
            'daily_engagement_pct': get_pct(d['engagement_leads_today'], d['touched_leads_today']),
            'daily_win_rate_pct': get_pct(d['won_today'], total_decided)
        }