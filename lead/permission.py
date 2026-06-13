from rest_framework.permissions import BasePermission

class IsInAnyGroup(BasePermission):
    """
    Custom permission to check if a user belongs to ANY group in a list.
    """

    group_names = []  # Class attribute to store group names

    def __init__(self, group_names=None):
        if group_names:
            self.group_names = group_names

    def has_permission(self, request, view):
        return request.user.groups.filter(name__in=self.group_names).exists()

    @classmethod
    def for_groups(cls, group_names):
        """
        Factory method to create a new permission class for specific groups.
        """
        return type(f"IsInGroup_{'_'.join(group_names)}", (cls,), {"group_names": group_names})
