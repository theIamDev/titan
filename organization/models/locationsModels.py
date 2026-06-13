from django.db import models
from organization.models.orgsModels import Organizations
from .locationsManager import LocationManager

# Location (Branch) Model
class Locations(models.Model):
    organization = models.ForeignKey(Organizations, on_delete=models.CASCADE, related_name="locations")
    name = models.CharField(max_length=255)
    description = models.TextField()
    address = models.TextField()
    created_dt = models.DateTimeField(auto_now_add=True)
    last_updated_dt = models.DateTimeField(auto_now=True)

    object = LocationManager()

    def __str__(self):
        return f"{self.name} - {self.organization.name}"