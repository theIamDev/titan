from typing import List, Set, Dict, Any
from django.db.models import CharField, Value, IntegerField, F
from django.db.models.functions import Coalesce
from django.db.models import OuterRef, Subquery
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

# Models
from ...models.subUserAccountModels import sub_users_account
from ...models.usersAccountModels import Users_account
# from employee.models import AliasUsername

User = get_user_model()

"""
all userlevel query functions for 1 db hit queries
"""

class UserService:
    @staticmethod
    def get_users_profiles_list(user):
        return sub_users_account.objects.for_user(user).filter(user__is_active=True).prefetch_related('user')  # type: ignore
    
    @classmethod
    def get_user_profile(cls, user, user_profile_id):
        """
        it returns single user details for which client has requested, by validating which client(user) has requested
        """
        return cls.get_users_profiles_list(user).filter(user_id=user_profile_id) 

    @staticmethod
    def get_context_map_users(requested_by_user, user_ids: List[int]) -> Dict[int, Dict[str, Any]]:
        if not user_ids:
            return {}

        # Subquery for user roles
        group_subquery = Group.objects.filter(user__id=OuterRef('user_id')).values('name')[:1]

        users_data = (
            sub_users_account.objects.for_user(requested_by_user) # type: ignore
            .filter(user_id__in=user_ids)
            .select_related('user', 'organization', 'location')
            .annotate(
                mapped_user_id=F('user_id'),
                display_name=Coalesce('full_name', 'user__username', output_field=CharField()),
                profile_first_name=Coalesce('first_name', 'user__username', output_field=CharField()),
                profile_last_name=Coalesce('last_name', Value(''), output_field=CharField()),
                email=F('user__email'),
                
                # Organization fields
                user_organization=Coalesce('organization_id', Value(0), output_field=IntegerField()),
                user_organization_name=Coalesce('organization__name', Value(''), output_field=CharField()),
                
                # Location fields
                user_location=Coalesce('location_id', Value(0), output_field=IntegerField()),
                user_location_name=Coalesce('location__name', Value(''), output_field=CharField()),
                user_account=Coalesce('account', Value(0), output_field=IntegerField()),
                user_role=Subquery(group_subquery)
            )
            .values(
                'mapped_user_id', 
                'display_name', 
                'profile_first_name', 
                'profile_last_name', 
                'email', 
                'user_organization', 
                'user_organization_name',
                'user_location',
                "user_account",
                'user_location_name',
                'user_role'
            )
        )

        return {u['mapped_user_id']: u for u in users_data}

    @classmethod
    def get_context_map_user(cls, requested_by_user, user_id: int):
        res = cls.get_context_map_users(requested_by_user, [user_id])
        return res.get(user_id, {})
    
    @classmethod
    def get_direct_reportees(cls, requested_by_user, supervisor_user_id: int):
        """
        returns subquery for all direct reportees scoped by requesting user
        """
        return sub_users_account.objects.for_user(requested_by_user).filter( # type: ignore
            supervisor_id=supervisor_user_id
        ).values('user_id')
    
    @staticmethod
    def resolve_user_username(identifiers: Set[str]) -> Dict[str, int]:
        if not identifiers:
            return {}

        users = User.objects.filter(username__in=identifiers).values("id", "username")
        lookup = {u["username"]: u["id"] for u in users}

        # remaining = identifiers - set(lookup.keys())
        # if remaining:
        #    aliases = AliasUsername.objects.filter(username__in=remaining).values("user_id", "username")
        #    lookup.update({a["username"]: a["user_id"] for a in aliases})

        return lookup