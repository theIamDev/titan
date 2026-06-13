from django.db import models
from .activityTimelineManager import ActivityTimelineManager

class ActivityTimelineLog(models.Model):
    object_identifier = models.IntegerField()
    activity_type = models.CharField(max_length=50)
    changes = models.JSONField()
    description = models.TextField(blank=True, null=True, help_text="Optional description or notes.")
    created_by = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, help_text="Record creation timestamp.")
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

    objects = ActivityTimelineManager()