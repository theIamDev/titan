from django.db import transaction
from django.contrib.auth.models import User, Group
from ....models.subUserAccountModels import sub_users_account
from packages.formatParsers.phoneNumberParser import validate_and_format_phone_number

from ..userServices import UserService

class CreateUser:

    DEFAULT_PASSWORD = "letmeconnect"

    def __init__(self, requested_by_user, params):
        self.requested_by_user = requested_by_user
        self.params = params

    def create(self):
        try:
            with transaction.atomic():
                # 1. Get Context info for the requester
                # This ensures we get organization/location/account data
                context = UserService.get_context_map_user(
                    self.requested_by_user, 
                    self.requested_by_user.id
                )

                # 2. Logic for Organization and Location
                # Organization is always the same as the requester
                org_id = context.get('user_organization')
                
                # Location logic: 
                # If admin -> requester's location. 
                # If super_admin -> location from request body.
                if context.get('user_role') == 'super_admin':
                    loc_id = self.params.get('location_id')
                else:
                    loc_id = context.get('user_location')
                user_password = self.params.get('password',self.DEFAULT_PASSWORD)
                user_username = self.params.get('email')
                raw_mobile = self.params.get('mobile')
                try:
                    parsed_mobile = validate_and_format_phone_number(raw_mobile)
                except:
                    parsed_mobile = str(raw_mobile)
                # 3. Create the Base Auth User
                new_user = User.objects.create_user(
                    username=user_username,
                    email=self.params.get('email'),
                    password=user_password,
                    first_name=self.params.get('first_name'),
                    last_name=self.params.get('last_name')
                )

                # 4. Handle Group/Role Assignment (auth_user_groups)
                role_id = self.params.get('role_id')
                if role_id:
                    group = Group.objects.filter(id=role_id).first()
                    if group:
                        new_user.groups.add(group)

                # 5. Create the Sub-User Profile (account_sub_users_account)
                # Note: We use the IDs directly to avoid unnecessary model lookups
                profile = sub_users_account.objects.create(
                    user=new_user,
                    first_name=self.params.get('first_name'),
                    middle_name=self.params.get('middle_name'),
                    last_name=self.params.get('last_name'),
                    mobile=parsed_mobile,
                    supervisor_id=self.params.get('supervisor_id'),
                    account=context.get('user_account', 1),
                    organization_id=org_id,
                    location_id=loc_id
                )
                return {"username":user_username,"password":user_password}

        except Exception as e:
            # transaction.atomic() will rollback on error
            print(f"Error creating user: {str(e)}")
            raise ValueError(f"Error creating user: {str(e)}")