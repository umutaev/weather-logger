from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


class DatarecordModel(models.Model):
    class RecordType(models.TextChoices):
        TEMPERATURE = "TEMPERATURE"
        HUMIDITY = "HUMIDITY"
        PRESSURE = "PRESSURE"

    label = models.CharField(max_length=256, null=True, default=None)
    value = models.IntegerField(blank=False, null=False)
    type = models.CharField(choices=RecordType.choices, max_length=11)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.DO_NOTHING, related_name="records"
    )
    creation_date = models.DateTimeField(editable=False)
    date = models.DateTimeField(null=True)

    def save(self, *args, **kwargs) -> None:
        if not self.id:
            self.creation_date = timezone.now()
            if not self.date:
                self.date = self.creation_date
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.get_type_display()} with "{self.label}" label and value of {self.value} posted by {self.user.username}'
