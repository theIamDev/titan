from ....models.lead import Lead
from account.services.users.userServices import UserService
from packages.formatParsers.phoneNumberParser import validate_and_format_phone_number

# utitlity imports
from ...utils.hashing import Hashing  
from ....models.ActivityTimelineLogModel import ActivityTimelineLog
from ...timeline.createTimeline import timeline_save
from django.db import transaction


class CreateService:
    def __init__(self, user,user_cache, data,is_bulk, sess_id):
        self.user = user
        # Local memory cache for the duration of this request
        self.user_cache = user_cache
        self.data = data
        self.sess_id = sess_id     
        self.is_bulk = is_bulk

    def execute(self):
        try:
            lead_instances = self._transform()
            msg = "Lead importing stated"
            count = len(lead_instances)
            lead_id = None
            msg,lead_id,count = self.__database_create(lead_instances)
            return True, msg, lead_id, count
        except Exception as e:
            return False, str(e), None, None
        
    def __database_create(self,lead_instances):
        if self.is_bulk:
            with transaction.atomic():
                bulk_created = Lead.objects.bulk_create(lead_instances)
                created_leads = Lead.objects.filter(sess_id=self.sess_id).order_by("-id")[: len(bulk_created)]
                self._trigger_timeline(created_leads)
            msg = "Lead imported successfully"
            count = len(bulk_created)
            lead_id = None
        else:
            with transaction.atomic():
                created_lead = lead_instances[0]
                created_lead.save()
                self._trigger_timeline([created_lead])
            msg = "lead created successfully"
            lead_id = created_lead.id
            count = 1
        return msg,lead_id,count

    
    def _trigger_timeline(self, leads):
        current_user_name = self.user_cache.get(self.user.id, {}).get("display_name", "System")
        desciption = "Lead is imported by "+current_user_name if self.is_bulk else "Lead created by "+current_user_name
        user_details = self.user_cache.get(self.user.id)
        log_instances = [
            ActivityTimelineLog(
                object_identifier=lead.id,
                activity_type="Lead Creation",
                changes={
                    "lead_status_id": {"to": lead.lead_status_id, "from": None},
                    "assigned_to": {"to": lead.assigned_to, "from": None}
                },
                description=desciption,
                created_by=self.user.id,
                location_id = user_details.get('user_location',None),
                organization_id = user_details.get('user_organization',None)
            ) for lead in leads
        ]
        return timeline_save(log_instances)

    def _transform(self) -> list:
        lead_data_list = self.data.get("leadlist", [])
        if not isinstance(lead_data_list, list) or not lead_data_list:
            raise ValueError("Invalid lead data provided")

        # 1. Constants & Context Prefetch
        NEW_STATUS, QUEUE_STATUS = 1, 2
        NEW_STAGE, NEW_STATE = 1, "active"
        current_user_id = self.user.id
        
        # 2. Bulk Resolution
        raw_assigned_values = {d.get("assigned_to") for d in lead_data_list if d.get("assigned_to")}
        resolved_id_map = self._resolve_assigned_to(list(raw_assigned_values))
        
        unique_ids_to_fetch = set(resolved_id_map.values())
        unique_ids_to_fetch.add(current_user_id)
        
        self.user_cache.update(UserService.get_context_map_users(self.user,list(unique_ids_to_fetch)))
        current_user_ctx = self._get_user_info(current_user_id)

        incoming_hashes = {self.__calc_hash_key(d.get("contact")) for d in lead_data_list}

        existing_hashes = set(
        Lead.objects.filter(hash_key__in=incoming_hashes)
        .values_list('hash_key', flat=True)
        )

        # 3. Process & Deduplicate
        seen_hashes = set()
        lead_instances = []

        # Process in REVERSE to keep the 'latest' lead if duplicates exist 
        # (Matching your previous _remove_duplicates_if_any logic)
        source_value = "bulk import" if len(lead_data_list) > 1 else "direct"
        for data in reversed(lead_data_list):
            contact = data.get("contact", "")
            contact_str = str(contact).strip()
            try:
                parsed_contact = validate_and_format_phone_number(contact_str)
            except:
                parsed_contact = str(contact_str)
            hash_key = self.__calc_hash_key(parsed_contact)
            if hash_key in seen_hashes:
                continue
            seen_hashes.add(hash_key)
            golden = 'du' if hash_key in existing_hashes else 'go'
            raw_assigned = data.get("assigned_to")
            assigned_id = resolved_id_map.get(raw_assigned)
            
            ctx = self.user_cache.get(assigned_id) if assigned_id else current_user_ctx
            user_details = self.user_cache.get(self.user.id)
            prepared_data = {
                **data,
                "hash_key": hash_key,
                "valid_contact":parsed_contact,
                "golden": golden,
                "assigned_to": assigned_id,
                "source_assigned": raw_assigned,
                "created_by": current_user_id,
                "last_updated_by": current_user_id,
                "state": NEW_STATE,
                "lead_status_id": NEW_STATUS if assigned_id else QUEUE_STATUS,
                "lead_stage_id": NEW_STAGE,
                "sess_id": self.sess_id,
                "account": ctx.get("account_id") or ctx.get("user_account", 0),
                "location_id": user_details.get("location_id") or user_details.get("user_location", 0),
                "organization_id": user_details.get("organization_id") or user_details.get("user_organization", 0),
                "priority": data.get("priority") or "cold",
                "source": data.get("source") or source_value
            }
            lead_instances.append(Lead(**prepared_data))

        return lead_instances[::-1]

    def _resolve_assigned_to(self, raw_values: list) -> dict:
        if not raw_values:
            return {}

        result_map = {}
        to_resolve_strings = set()

        for val in raw_values:
            if not val:
                continue
            item_str = str(val).strip()
            if item_str.isdigit():
                result_map[val] = int(item_str)
            else:
                to_resolve_strings.add(item_str)

        if to_resolve_strings:
                resolved_strings = UserService.resolve_user_username(to_resolve_strings)
                result_map.update(resolved_strings)
        return result_map

    def _get_user_info(self, user_id):
        if not user_id:
            return {}
        # Check local cache (highly optimized for loops)
        if user_id not in self.user_cache:
            self.user_cache.update(UserService.get_context_map_users(self.user,[user_id]))
        ctx = self.user_cache.get(user_id, {})
        return ctx
    
    def __calc_hash_key(self,*params):
        hash_key = Hashing(params).hash()
        return hash_key
    

