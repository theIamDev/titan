import csv
from ...models import Lead
from ...filters.leadFilters import LeadFilter

class Echo:
    """Pass-through buffer for csv.writer."""
    def write(self, value):
        return value

class LeadExportService:
    def __init__(self, user, params: dict):
        self.user = user
        self.params = params
        self.writer = csv.writer(Echo())

    def _get_filtered_queryset(self):
        """Applies permissions and filters to the Lead model."""
        # Use your custom manager 'for_user' for security
        queryset = Lead.objects.for_user(self.user).order_by('-created_dt', 'id') # type: ignore
        
        # Apply Django-filter logic
        filterset = LeadFilter(self.params, queryset=queryset)
        if not filterset.is_valid():
            return Lead.objects.none()
        return filterset.qs

    def stream_csv(self):
        """A generator that yields CSV rows one by one."""
        # 1. Use values_list for O(1) memory overhead and speed
        queryset = self._get_filtered_queryset().values_list(
            'id', 'name', 'email', 'lead_status__name', 'created_dt'
        ).iterator(chunk_size=2000)

        # 2. Yield Header
        yield self.writer.writerow(['ID', 'First Name', 'Last Name', 'Email', 'Status', 'Created At'])

        # 3. Yield Rows
        for row in queryset:
            yield self.writer.writerow(row)

    def get_file_name(self):
        return "leads_export.csv"