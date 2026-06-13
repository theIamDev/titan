from django.db.models import Count
from .BaseAnalyticsBuilder import BaseAnalyticsBuilder
from ...models.lead import Lead

class ConversionDistribution(BaseAnalyticsBuilder):
    def get_initial_queryset(self):
        return Lead.objects.for_user(self.user) # type: ignore

    def apply_annotations(self):
            stats = self.queryset.filter( # type: ignore
                lead_status_id__in=[13, 14, 15]
            ).values('lead_status_id').annotate(total=Count('id'))

            # Map IDs to semantic keys, not colors
            status_map = {
                13: "won",
                14: "lost",
                15: "invalid",
            }
            self.queryset = [
                {
                    "status_id": item['lead_status_id'],
                    "type": status_map.get(item['lead_status_id'], "other"),
                    "count": item['total']
                } for item in stats
            ]
            return self