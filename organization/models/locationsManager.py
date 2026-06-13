from django.db import models
from account.services.users.userServices import UserService

class LocationManager(models.Manager):
    def for_user(self, user):
        try:
            user_groups = set(user.groups.values_list('name', flat=True))
            queryset = self.get_queryset()
            user_details = UserService.get_context_map_user(user,user.id)
            org_id = user_details.get('user_organization',None)
            if not org_id:
                    raise ValueError('no org or loc')
            if "system_admin" in user_groups:
                return queryset
            if "super_admin" in user_groups:
                return queryset.filter(organization = org_id)
            return self.get_queryset().none()
        except Exception as e:
            return self.get_queryset().none() 

