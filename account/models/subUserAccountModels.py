from django.db import models
from django.contrib.auth.models import User  # Using Django's default User model
from .subUserManager import SubUserManager

# User Profile Model (Admin & Sub-User Roles)
class sub_users_account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")  
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=300, null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    supervisor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="sub_users")  # Only for Sub-Users
    account = models.IntegerField(default=1)
    organization = models.ForeignKey(
        'organization.Organizations', 
        on_delete=models.PROTECT,
        db_column='organization'
    )
    location = models.ForeignKey(
        'organization.Locations', 
        on_delete=models.PROTECT,
        db_column='location'     
    ) 

    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)

    objects = SubUserManager()

    def __str__(self):
        return f"{self.full_name} ({self.user.username})"

    def save(self, *args, **kwargs):
        self.full_name = f"{self.first_name} {self.middle_name or ''} {self.last_name}".strip()
        super(sub_users_account, self).save(*args, **kwargs)
