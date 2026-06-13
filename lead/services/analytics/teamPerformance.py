from django.db.models import Count, F
from account.services.users.userServices import UserService
from ..timeline.getTimeline import GetTimelineService


class TeamPerformance():
    def __init__(self, user, params):
        self.user = user
        self.params = params

    @staticmethod
    def get_user_actions(queryset):
        return queryset.filter(activity_type="Lead Action")

    def get(self):
        # HIT 1: Fetch user IDs and Names in one go. 
        # Using .values() converts model objects to dicts, solving the 'subscriptable' error.
        users = (
            UserService.get_users_profiles_list(self.user)
            .values('user_id', 'full_name')
        )
        
        user_ids = [u['user_id'] for u in users]

        # HIT 2: Aggregate distinct lead touches for all users in one grouping query.
        queryset = GetTimelineService(self.user,self.params).get_queryset()
        activity_counts = (
            queryset.filter(
                created_by__in=user_ids,
                activity_type="Lead Action"
            )
            .order_by()
            .values('created_by')
            .annotate(distinct_touches=Count('object_identifier', distinct=True))
        )
        # Create a lookup map for O(1) access
        count_map = {item['created_by']: item['distinct_touches'] for item in activity_counts}

        # Stacking the data for the frontend
        final_performance = []
        for u in users:
            # Construct name from available fields
            full_name = u['full_name']
            display_name = full_name if full_name else "unknown"
            
            final_performance.append({
                "id": u['user_id'],
                "name": display_name,
                "touches": count_map.get(u['user_id'], 0)
            })

        # Sort by performance (Top Touches)
        return sorted(final_performance, key=lambda x: x['touches'], reverse=True)
    
