from ...models.ldcntrlModel import Ldcntrl

class LoadControl:
    def __init__(self,user) -> None:
        self.user = user
        self.queryset = self._initial_queryset()
        

    def get(self):
        return self.queryset

    def _initial_queryset(self):
        return Ldcntrl.objects.for_user(self.user).filter(load_type='bulk entry').order_by("-sess_id")  # type: ignore