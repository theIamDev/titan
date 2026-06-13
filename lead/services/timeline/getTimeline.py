from typing import Any, Dict, Optional
from django.db.models import QuerySet
from ...models.ActivityTimelineLogModel import ActivityTimelineLog
from ...filters.activitylogFilters import ActivityLogFilter

class GetTimelineService:
    """
    Handles fetching and preparing lead activity logs.
    Returns a QuerySet to allow for deferred execution and pagination.
    """

    def __init__(self, user: Any, data: Dict[str, Any]):
        self.user = user
        self.data = data

    def get_queryset(self) -> QuerySet:
        """
        Returns a filtered QuerySet of ActivityTimelineLog.
        Business logic for hydration is deferred to the caller or serializer.
        """
        if not self.data:
            self.data = {}

        # select_related reduces DB hits if created_by was a FK. 
        # Since it's currently an integer, we maintain the base queryset.
        queryset = ActivityTimelineLog.objects.for_user(self.user).all().order_by('-created_at') # type: ignore
        # Apply filters
        filtered_set = ActivityLogFilter(self.data, queryset=queryset)

        return filtered_set.qs

    @staticmethod
    def hydrate_timeline_data(user,activities: QuerySet) -> list:
        """
        Ancillary method to perform bulk lookup and hydration 
        after the QuerySet has been sliced (e.g., after pagination).
        """
        # 1. Collect IDs from the materialized slice only (O(k) where k is page size)
        user_ids = set()
        status_ids = set()
        stage_ids = set()

        for activity in activities:
            if isinstance(activity.created_by, int):
                user_ids.add(activity.created_by)
            
            changes = activity.changes or {}
            for field in ['lead_status_id', 'lead_stage_id', 'assigned_to']:
                node = changes.get(field)
                if node:
                    for key in ('from', 'to'):
                        val = node.get(key)
                        if isinstance(val, int):
                            if field == 'lead_status_id': status_ids.add(val)
                            elif field == 'lead_stage_id': stage_ids.add(val)
                            else: user_ids.add(val)

        # 2. Bulk fetch mappings
        from ...models.lead import Stage, Status
        from account.services.users.userServices import UserService

        status_map = dict(Status.objects.filter(id__in=status_ids).values_list('id', 'name'))
        stage_map = dict(Stage.objects.filter(id__in=stage_ids).values_list('id', 'name'))
        user_map = UserService.get_context_map_users(user,list(user_ids))

        # 3. Format result
        results = []
        for a in activities:
            # Internal hydration logic (reusing your logic)
            resolved_changes = (a.changes or {}).copy()
            
            # Helper for name injection
            def inject_names(node, mapping):
                if node:
                    node['from_name'] = mapping.get(node.get('from'), "Unknown")
                    node['to_name'] = mapping.get(node.get('to'), "Unknown")

            inject_names(resolved_changes.get('lead_status_id'), status_map)
            inject_names(resolved_changes.get('lead_stage_id'), stage_map)
            
            user_lookup = {k: v.get('display_name') for k, v in user_map.items()}
            inject_names(resolved_changes.get('assigned_to'), user_lookup)

            user_info = user_map.get(a.created_by)
            results.append({
                "id": a.id,
                "leadid":a.object_identifier,
                "activity_type": a.activity_type,
                "changes": resolved_changes,
                "description": a.description,
                "created_at": a.created_at,
                "created_by_id": a.created_by,
                "created_by_name": user_info.get("display_name", "System") if user_info else "System"
            })
        return results