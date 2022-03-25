from django.contrib import admin
from data.models import DatarecordModel, TemperatureModel, HumidityModel, PressureModel

admin.site.register(DatarecordModel)
admin.site.register(TemperatureModel)
admin.site.register(HumidityModel)
admin.site.register(PressureModel)
