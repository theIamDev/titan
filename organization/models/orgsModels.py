from django.db import models
import uuid
from django.contrib.auth import get_user_model  # Avoids circular import issues

User = get_user_model()

# Organization (Business Entity) Model
class Organizations(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_dt = models.DateTimeField(auto_now_add=True)
    last_updated_dt = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name


