from ...models.workflowModels import Stage, Status
from django.db.models import Prefetch


class LeadPipelineService:

    def __init__(self,user) -> None:
        self.user = user
        self.queryset = self._initial_query()

    def get_pipeline(self):
        return self.queryset

    def _initial_query(self):
        status_queryset = Status.objects.filter(is_active = True).order_by('sort_order')
        pipeline = Stage.objects.prefetch_related(
                Prefetch('statuses', queryset=status_queryset)
            ).filter(is_active = True).order_by('order')
        return pipeline
        