from django.db import models

class Task(models.Model):
    object_id = models.IntegerField(blank = False, null = True)
    task_date = models.DateTimeField(blank=False,null=True)
    timestamp =  models.DateTimeField(blank=False,null=True)
    user_id = models.IntegerField(blank = False, null = True)
    active = models.BooleanField()
    reason = models.CharField(blank=False,null=True,max_length=1000)
    description = models.CharField(blank=False,null=True,max_length=1000)
    system_generated = models.CharField(blank=False,null=True,max_length=100)
    task_complete_description =  models.CharField(blank=False,null=True,max_length=100)