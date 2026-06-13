from django.db import models
from .ldcntrlModelManager import LDCNTRLManager

class Ldcntrl(models.Model):
    sess_id = models.BigAutoField(primary_key=True)  # Auto-incrementing unique ID
    LOAD_TYPE_CHOICES = [
        ('Bulk Import', 'Bulk Import'),
        ('API', 'API'),
        ('Manual Entry', 'Manual Entry'),
    ]
    load_type = models.CharField(max_length=50, choices=LOAD_TYPE_CHOICES, null=True, blank=True)
    load_status = models.BooleanField(default=False)
    count = models.IntegerField(null=True, blank=True, default=0)
    source_name = models.CharField(max_length=200, null=True, blank=True)
    load_timestamp = models.DateTimeField(auto_now_add=True)
    account = models.IntegerField(blank = False, null = True)
    organization = models.ForeignKey(
        'organization.Organizations', 
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_column='organization'
    )
    location = models.ForeignKey(
        'organization.Locations', 
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_column='location'     
    )

    objects = LDCNTRLManager()

    def __str__(self):
        return f"Session {self.session_id} - {self.load_type}" # type: ignore
