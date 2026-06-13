from ....models.subUserAccountModels import sub_users_account

class UserGetService():
    def __init__(self,user,params) -> None:
        self.user = user
        self.params = params
        self.queryset = self._initial_queryset()

    def get_user_list(self):
        self._apply_params()
        return self.queryset

    def get_user(self,user_id):
        return self.queryset.filter(user_id = user_id)

    def _initial_queryset(self):
        return sub_users_account.objects.for_user(self.user).select_related("user").order_by("-id") # type: ignore

    def _apply_params(self):
        is_active = self.params.get('is_active',True)
        value = True
        if is_active != 'true':
            value = False
        self.queryset = self.queryset.filter(user__is_active=value)