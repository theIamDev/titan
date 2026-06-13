from account.services.users.userServices import UserService

class OwnerGetService():
    def __init__(self,user) -> None:
        self.user = user

    def get_users_list(self):
        return UserService.get_users_profiles_list(self.user)

    def get_user(self,user_id):
        return UserService.get_user_profile(self.user,user_id)
