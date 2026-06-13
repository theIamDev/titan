from django.db import models
from django.contrib.auth.models import User

class Users_account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="business_account")
    name = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)

    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Account Owner: {self.user.email}"
