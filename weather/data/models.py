from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from typing import Optional, Iterable


class DatarecordModel(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.DO_NOTHING, related_name="data"
    )
    creation_date = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs) -> None:
        if not self.id:
            self.creation_date = timezone.now()
        return super().save(*args, **kwargs)


class TemperatureModel(models.Model):
    value = models.IntegerField(blank=False, null=False)
    label = models.CharField(max_length=256, blank=False, null=True, default=None)
    record = models.ForeignKey(
        DatarecordModel, on_delete=models.CASCADE, related_name="temperature"
    )


class HumidityModel(models.Model):
    value = models.IntegerField(blank=False, null=False)
    label = models.CharField(max_length=256, blank=False, null=True, default=None)
    record = models.ForeignKey(
        DatarecordModel, on_delete=models.CASCADE, related_name="humidity"
    )


class PressureModel(models.Model):
    value = models.IntegerField(blank=False, null=False)
    label = models.CharField(max_length=256, blank=False, null=True, default=None)
    record = models.ForeignKey(
        DatarecordModel, on_delete=models.CASCADE, related_name="pressure"
    )
