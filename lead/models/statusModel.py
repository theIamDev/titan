from django.db import models

class Lead_Status(models.Model):
    status = models.CharField(blank=False,null=True,max_length=100)
    discription = models.CharField(blank=False,null=True,max_length=1000)
    system_generated = models.CharField(blank=False,null=True,max_length=100)
    stage = models.CharField(blank=False,null=True,max_length=100)

    sys_new_code = "SYS_New"
    sys_call_back_code = "SYS_Call_Back"
    sys_meeting_planned = "SYS_Meeting Planned"
    sys_site_visit = "SYS_SITE_VISIT"
    follow_up_meeting = "SYS_FOLLOW_UP_MEETING"
    sys_closed = "SYS_CLOSED"

    def create_status(self,status_name,description):
        system_generated = "USR_"+status_name
        try:
            lead_obj = self.objects.create(status = status_name,discription = description,system_generated = system_generated)
            return True
        except:
            return False


    def delete_by_id(self,id):
        try:
            Lead_Status.objects.get(id = id).delete()
            return True
        except:
            return False
        


"""

class status():

    sys_new_code = "SYS_New"
    sys_call_back_code = "SYS_Call_Back"
    sys_meeting_planned = "SYS_Meeting Planned"
    sys_site_visit = "SYS_SITE_VISIT"
    follow_up_meeting = "SYS_FOLLOW_UP_MEETING"
    sys_closed = "SYS_CLOSED"

    def create_status(self,status_name,description):
        system_generated = "USR_"+status_name
        try:
            lead_obj = Lead_Status.objects.create(status = status_name,discription = description,system_generated = system_generated)
            return True
        except:
            return False


    def delete_by_id(self,id):
        try:
            Lead_Status.objects.get(id = id).delete()
            return True
        except:
            return False

    def lead_to_status(self,request,lead_id,status_id,priority):
        lead_obj = lead_db.objects.get(id = lead_id)
        comment = ''
        if(status_id == None):
            status_id = lead_obj.status
        status_obj = Lead_Status.objects.get(id = status_id)

        if(lead_obj.status != status_id):
            lead_obj.status = status_id
            comment = comment + 'Status has been changed to <b>' +status_obj.status +'</b> </br> '
        if(lead_obj.priority != priority):
            comment = comment+ 'Priority has been changed to <b>'  +priority + '</b>'
            lead_obj.priority = priority

        if(comment != ''):
            timeline_db.objects.create(lead_id=lead_obj.id,timestamp=localtime(now()),comment = comment,status_id = status_obj.id,user_id=request.user.id)

        lead_obj.save()
        return True

    def lead_to_callback_status(self,request,lead_id,status_id):
        try:
            lead_obj = lead_db.objects.get(id = lead_id)
        except ObjectDoesNotExist:
            return False
        try:
            status_obj = Lead_Status.objects.get(id = status_id)
        except ObjectDoesNotExist:
            return False

        lead_obj.status = status_id
        lead_obj.save()
        Timeline().auto_system_status_comment(request,status.sys_call_back_code,lead_obj)
        return True

    def lead_to_meeting_status(self,request,lead_id,status_id):
        try:
            lead_obj = lead_db.objects.get(id = lead_id)
        except ObjectDoesNotExist:
            return False
        try:
            status_obj = Lead_Status.objects.get(id = status_id)
        except ObjectDoesNotExist:
            return False

        lead_obj.status = status_id
        lead_obj.save()
        task_obj = Timeline().auto_system_status_comment(request,status_obj.system_generated,lead_obj)
        return task_obj


        return True

    def system_status(self):
        all_status = Lead_Status.objects.all()
        sys_new = False
        sys_call_back = False
        for status_obj in all_status:
            if status_obj.system_generated == status().sys_new_code:
                sys_new = True
            if status_obj.system_generated == status().sys_call_back_code:
                sys_call_back = True

        if(sys_new == False):
            Lead_Status.objects.create(status = "New",discription = "This is a System generated Status.",system_generated = status().sys_new_code)

        if(sys_call_back == False):
            Lead_Status.objects.create(status = "Call Back",discription = "This is a System generated Status.",system_generated = status().sys_call_back_code)

        return True

    def system_status_check(self,status_id):
        try:
            status_obj = Lead_Status.objects.get(id = status_id)
        except ObjectDoesNotExist:
            return True

        if(status_obj.system_generated[0:3] == 'SYS'):
            return True

        return False

"""
