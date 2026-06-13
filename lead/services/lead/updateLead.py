from ...models.lead import Lead
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from ..timeline.createTimeline import timeline_save
from account.services.users.userServices import UserService
# from django.contrib.auth import get_user_model
# User = get_user_model()

def lead_update(user,data):
    try:
        if not data:
            return {'success':False,'msg':'No data present'}
        
        lead_id = data.get('id', None)

        if not lead_id:
            return {'success':False,'msg':'No data present'}

        try:
            lead_instance = Lead.objects.get(id=lead_id)
        except ObjectDoesNotExist:
            return {'success':False,'msg':'Lead not found'}

        # Track changes for timeline
        changes = {}

        for key, value in data.items():
            if hasattr(lead_instance, key):

                if key == 'assigned_to' or key == 'lead_status_id' or key == 'priority':
                    continue

                old_value = getattr(lead_instance, key)
                new_value = value
                if str(old_value) != str(new_value):  
                    changes[key] = {"from": old_value, "to": new_value}
                    setattr(lead_instance, key, new_value)

        if not changes:
            return {'success':True,'msg':'No changes Found','lead_id':lead_id}

        with transaction.atomic():
            lead_instance.last_updated_by = user.id
            lead_instance.save()
            update_timeline(user, lead_instance, changes)

        return {'success':True,'msg':'Lead updated successfully','lead_id':lead_id}

    except Exception as e:
        return {'success':False,'msg':str(e)}

def update_timeline(user, lead_instance, changes):
    if not changes:
        return False
    user_details = UserService.get_context_map_user(user,user.id)
    log_data = {
        "object_identifier": lead_instance.id,
        "activity_type": "Lead Updated",
        "changes": changes,
        "description": "Lead details updated.",
        "created_by": user.id,
        "location_id" : user_details.get('user_location',None),
        "organization_id": user_details.get('user_organization',None),
    }
    activity_log = timeline_save(log_data)
    return activity_log.get('created', False)
