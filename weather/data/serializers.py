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
    temperature = TemperatureSerializer(many=True, required=False)
    humidity = HumiditySerializer(many=True, required=False)
    pressure = PressureSerializer(many=True, required=False)

    def create(self, validated_data):
        temperature = validated_data.pop("temperature", [])
        humidity = validated_data.pop("humidity", [])
        pressure = validated_data.pop("pressure", [])
        datarecord = DatarecordModel.objects.create(**validated_data)
        for instance in temperature:
            TemperatureModel.objects.create(record=datarecord, **instance)
        for instance in humidity:
            HumidityModel.objects.create(record=datarecord, **instance)
        for instance in pressure:
            PressureModel.objects.create(record=datarecord, **instance)
        return datarecord

    class Meta:
        model = DatarecordModel
        exclude = []
