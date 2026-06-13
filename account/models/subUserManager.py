from django.db import models
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)

class SubUserManager(models.Manager):
    def for_user(self, user):
        """
        Filters the SubUser queryset based on the requesting user's 
        permissions, organization, and location.
        """
        if not user or user.is_anonymous:
            return self.none()

        try:
            # 1. Fetch user context in one efficient hit
            # Assumes SubUser table contains the org/loc metadata for users
            user_info = self.filter(user_id=user.id).values('organization', 'location').first()
            
            if not user_info:
                return self.none()

            org_id = user_info.get('organization')
            loc_id = user_info.get('location')
            
            # 2. Define base queryset
            queryset = self.get_queryset()
            
            # 3. Check roles (ordered from most permissive to least)
            user_groups = user.groups.values_list('name', flat=True)

            if "system_admin" in user_groups:
                return queryset

            if "super_admin" in user_groups:
                return queryset.filter(organization=org_id)

            if "admin" in user_groups:
                return queryset.filter(organization=org_id, location=loc_id)

            if "viewer" in user_groups:
                # Optimized: Use values_list for the subquery to keep it in the DB
                reportee_ids = self.filter(supervisor_id=user.id).values_list('user_id', flat=True)
                return queryset.filter(
                    Q(user_id__in=reportee_ids) | Q(user_id=user.id),
                    organization=org_id,
                    location=loc_id
                ).distinct()

            # Default: No matching roles
            return self.none()

        except Exception as e:
            logger.error(f"Error filtering SubUsers for user {user.id}: {e}")
            return self.none()