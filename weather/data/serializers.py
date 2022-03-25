from rest_framework import serializers
from data.models import DatarecordModel, TemperatureModel, HumidityModel, PressureModel


class TemperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemperatureModel
        exclude = ["id", "record"]


class HumiditySerializer(serializers.ModelSerializer):
    class Meta:
        model = HumidityModel
        exclude = ["id", "record"]


class PressureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PressureModel
        exclude = ["id", "record"]


class DatarecordSerializer(serializers.ModelSerializer):
    temperature = TemperatureSerializer(many=True)
    humidity = HumiditySerializer(many=True)
    pressure = PressureSerializer(many=True)

    class Meta:
        model = DatarecordModel
        exclude = []
