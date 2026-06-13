# from .parseAnalyticsParams import parse_analytics_params
from ...filters.leadFilters import LeadFilter

class BaseAnalyticsBuilder:
    def __init__(self, user, params):
        self.user = user
        self.params = params
        self.queryset = self.get_initial_queryset()
        self.filterset = None

    def get_initial_queryset(self):
        raise NotImplementedError("Each report must define its starting table.")

    def build(self):
        """
        The standard execution flow (The Infrastructure Pipeline)
        """
        self._apply_filter()
        return (self
                .apply_annotations()
                .apply_post_filters()
                .queryset)
    
    def _apply_filter(self):
        self.filterset = LeadFilter(self.params, queryset=self.queryset)
        if not self.filterset.is_valid():
            self.queryset = self.queryset.none()
        else:
            self.queryset = self.filterset.qs
    
    def apply_annotations(self): return self
    def apply_post_filters(self): return self