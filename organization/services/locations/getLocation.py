from ...models.locationsModels import Locations

class GetLocation:
    def __init__(self,user) -> None:
        self.user = user
        self.queryset = self.__initial_queryset()

    def __initial_queryset(self):
        return Locations.object.for_user(self.user).all()

    def locations_all(self):
        return self.queryset