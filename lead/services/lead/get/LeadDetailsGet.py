from typing import Optional, Dict, Any
from account.services.users.userServices import UserService
from ....models.lead import Lead

class LeadDetailService:
    def __init__(self, user, lead_id: int) -> None:
        self.user = user
        self.lead_id = lead_id

    def get(self) -> Optional[Dict[str, Any]]:
        queryset = self._get_lead_data()
        if not queryset:
            return None
        return queryset

    def _get_lead_data(self) -> Optional[Dict[str, Any]]:
        queryset = (
            Lead.objects.for_user(self.user) # type: ignore
            .filter(id=self.lead_id)
            .select_related('lead_status')
        )
        return queryset.first()

    def enrich_data(self, serialized_data: Dict[str, Any]) -> Dict[str, Any]:
            """Adds external user context to the dictionary."""
            assigned_id = serialized_data.get('assigned_to')
            
            if assigned_id:
                user_ctx = UserService.get_context_map_user(self.user,assigned_id)
                serialized_data['assigned_to'] = {"id":assigned_id,"name":user_ctx.get('display_name', 'Unknown')}
            return serialized_data