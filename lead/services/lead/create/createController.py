from ....models.ldcntrlModel import Ldcntrl
import logging
from .createService import CreateService
from account.services.users.userServices import UserService

logger = logging.getLogger("Lead create")

class LeadCreationController:
    def __init__(self, user, data):
        self.user = user
        self.user_cache = UserService.get_context_map_users(self.user,[user.id]) 
        self.data = data
        self.metadata = data.get('metadata', {})
        self.is_bulk = self._evaluate_creation_type()

    def create(self):
        try:
            session_id = self.metadata.get('session_id')
            if not session_id:
                session_id = self._create_session()
            if not session_id:
                return False,"Session was not initiated", None
            
            success,message,lead_id, count = CreateService(
                self.user,
                self.user_cache,
                self.data,
                self.is_bulk, 
                session_id).execute()

            if success:
                self._update_session_success(session_id,count)
            
            return True, message,lead_id, count, session_id

        except Exception as e:
            logger.error(f"Lead creation failed: {e}", exc_info=True)
            return False, str(e), None,  0, 0

    def _evaluate_creation_type(self):
        lead_list = self.data.get('leadlist', [])
        count = len(lead_list)
        return True if count > 1 else False

    def _create_session(self):
        load_type = self.metadata.get('loadtype')
        source_name = self.metadata.get('sourcename')
        u_ctx = self.user_cache.get(self.user.id, {})
        if not load_type or not source_name:
            return None

        sess_instance = Ldcntrl.objects.create(
            load_type=load_type, 
            source_name=source_name,
            account=u_ctx.get('user_account'),
            organization_id =u_ctx.get('user_organization'),
            location_id = u_ctx.get('user_location')
        )
        return sess_instance.sess_id

    def _update_session_success(self, session_id,count):
        try:
            sess_instance = Ldcntrl.objects.for_user(self.user).get(sess_id=session_id) # type: ignore
            current_chunk = self.metadata.get('current_chunk')
            total_chunks = self.metadata.get('total_chunks') 
            if current_chunk == total_chunks:
                sess_instance.load_status = True
            sess_instance.count = (sess_instance.count or 0) + count
            sess_instance.save()
            return sess_instance.sess_id
        except:
            return None