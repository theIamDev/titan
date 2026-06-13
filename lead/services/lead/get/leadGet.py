# services/lead_service.py
from ....filters.leadFilters import LeadFilter
from ....models import Lead

class LeadGetService:

    def __init__(self,user,params) -> None:
        self.user = user
        self.params = params
        self.queryset = self._get_initial_queryset(user)

    def get(self):
        """
        The entry point (Execution Flow).
        """
        try:
            self._apply_filter()
            self._apply_post_filters()
        except Exception as e:
            print(str(e))

        return self.queryset

    def _get_initial_queryset(self, user):
        return Lead.objects.for_user(user).select_related('lead_status').order_by('-created_dt', 'id') # type: ignore
    
    def _apply_filter(self):
        filterset = LeadFilter(self.params, queryset=self.queryset)
        if not filterset.is_valid():
            self.queryset = self.queryset.none()
        self.queryset = filterset.qs

    def _apply_post_filters(self):
        pass