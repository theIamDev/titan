from django.db.models import Count
from ...models.workflowModels import Stage
from ...models.lead import Lead
from .BaseAnalyticsBuilder import BaseAnalyticsBuilder

class StagePipeline(BaseAnalyticsBuilder):
    def get_initial_queryset(self):
        # We start with the leads already filtered by the Base class
        return Lead.objects.for_user(self.user) # type: ignore

    def apply_annotations(self):
        """
        STRATEGY: 
        1. Fetch all master Stages for the user's organization.
        2. Group the current lead queryset by stage and status.
        3. Merge lead counts into the master Stage list so stages with 0 leads are included.
        """
        # Step 1: Get all Stages (Master List)
        # Assuming stages are scoped to organization or account
        master_stages = Stage.objects.filter(is_active = True).order_by('order')

        # Step 2: Get raw counts from the filtered Leads queryset
        lead_stats = self.queryset.values( # type: ignore
            'lead_stage_id',
            'lead_status_id',
            'lead_status__name',
            'lead_status__sort_order'
        ).annotate(
            count=Count('id')
        ).order_by('lead_status__sort_order')

        # Step 3: Map lead stats for quick lookup
        # Format: { stage_id: [{status_info}, ...] }
        stats_map = {}
        for row in lead_stats:
            s_id = row['lead_stage_id']
            if s_id not in stats_map:
                stats_map[s_id] = []
            
            stats_map[s_id].append({
                "id": row['lead_status_id'],
                "name": row['lead_status__name'] or "Unknown",
                "count": row['count']
            })

        # Step 4: Construct the final list using master_stages as the base
        final_pipeline = []
        for stage in master_stages:
            stage_id = stage.id # type: ignore
            statuses = stats_map.get(stage_id, [])
            
            # Calculate total leads for this stage
            stage_total = sum(s['count'] for s in statuses)

            final_pipeline.append({
                "id": stage_id,
                "name": stage.name,
                "total": stage_total,
                "statuses": statuses # Even if empty, the frontend gets []
            })

        # Set the queryset to our processed list
        self.queryset = final_pipeline
        
        return self