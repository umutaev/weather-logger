from rest_framework import serializers
from data.models import DatarecordModel


class DatarecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatarecordModel
        exclude = []
