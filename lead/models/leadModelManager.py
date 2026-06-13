from django.db import models
from django.db.models import Q
from account.services.users.userServices import UserService

class LeadManager(models.Manager):
    def for_user(self, user):
        try:
            user_groups = set(user.groups.values_list('name', flat=True))
            queryset = self.get_queryset().filter(golden='go').exclude(state='archived')
            user_details = UserService.get_context_map_user(user,user.id)
            org_id = user_details.get('user_organization',None)
            loc_id = user_details.get('user_location',None)
            if not org_id or not loc_id:
                raise ValueError('no org or loc')
            if "system_admin" in user_groups:
                return queryset
            if "super_admin" in user_groups:
                return queryset.filter(organization =org_id)
            if "admin" in user_groups:
                return queryset.filter(organization =org_id,location = loc_id)
            if "viewer" in user_groups:
                reportee_ids = UserService.get_direct_reportees(user,user.id)
                return queryset.filter(
                    Q(assigned_to__in=reportee_ids) | Q(assigned_to=user.id),organization =org_id,location = loc_id
                ).distinct()
            return self.get_queryset().none()

        except Exception as e:
            return self.get_queryset().none()