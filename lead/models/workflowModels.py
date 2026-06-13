from django.db import models


class Stage(models.Model):
    name = models.CharField(max_length=100, unique=True)
    order = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    is_closed_bucket = models.BooleanField(default=False)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=100, unique=True)
    sub_name = models.CharField(max_length=150, blank=True, null=True)
    sort_order = models.PositiveIntegerField(default=0)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name="statuses")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name