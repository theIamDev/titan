
# models
from ...models import Lead
from ...models import Status

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

# services
from ..timeline.createTimeline import timeline_save
from account.services.users.userServices import UserService

def lead_action(user, data):
    try:
        # precheck data
        if not data:
            return {'success':False,'msg':'No data present'}
        
        lead_id = data.get('id', None)

        if not lead_id:
            return {'success':False,'msg':'No data present'}
        
        try:
            lead_instance = Lead.objects.get(id=lead_id)
        except ObjectDoesNotExist:
            return {'success':False,'msg':'Lead not found'}
        
        # change calculation business logic
        # Track changes for timeline
        changes = {}
        description_value = data.get('description', None)
        activity_type = "Lead Action"
        for key, value in data.items():
            if key in ['id', 'description'] or not hasattr(lead_instance, key):
                continue     
            old_value = getattr(lead_instance, key)
            new_value = value

            if str(old_value or '') != str(new_value or ''):
                changes[key] = {"from": old_value, "to": new_value}
                setattr(lead_instance, key, new_value)

            # handle lead status update 
            if key == 'lead_status_id' and new_value:
                # Fetch the stage associated with the new status
                new_stage_id = Status.objects.filter(id=new_value).values_list('stage', flat=True).first()

                if lead_instance.lead_stage_id != new_stage_id: # type: ignore
                    changes['lead_stage_id'] = {
                    "from": lead_instance.lead_stage_id,  # type: ignore
                    "to": new_stage_id
                }
                # Update the instance
                lead_instance.lead_stage_id = new_stage_id     # type: ignore

        if not changes and not description_value :
            return {'success':False,'msg':'No changes Found','lead_id':lead_id}
        elif not changes:
            activity_type = "User comment"
        elif not description_value:
            return {'success':False,'msg':'Description value mandatory','lead_id':lead_id}

        # database write
        with transaction.atomic():
            lead_instance.last_updated_by = user.id
            lead_instance.save()
            update_timeline(user, lead_instance, changes,activity_type,description_value)

        return {'success':True,'msg':'Lead updated successfully','lead_id':lead_id}

    except Exception as e:
        return {'success':False,'msg':str(e)}

def update_timeline(user, lead_instance, changes,activity_type,description_value):
    user_details = UserService.get_context_map_user(user,user.id)
    loc_id = user_details.get('user_location',None)
    org_id = user_details.get('user_organization',None)
    log_data = {
        "object_identifier": lead_instance.id,
        "activity_type":activity_type ,
        "changes": changes,
        "description":description_value ,
        "created_by": user.id,
        "location_id" : loc_id,
        "organization_id": org_id,
    }
    activity_log = timeline_save(log_data)
    return activity_log.get('success', False)

