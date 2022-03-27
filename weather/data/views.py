from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from data.models import DatarecordModel, TemperatureModel, HumidityModel, PressureModel
from data.serializers import (
    DatarecordSerializer,
    TemperatureSerializer,
    HumiditySerializer,
    PressureSerializer,
)


class DataView(ListAPIView, CreateAPIView):
    queryset = DatarecordModel.objects.all()
    permissions_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = DatarecordSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "user",
        "temperature__label",
        "humidity__label",
        "pressure__label",
    ]

    def create(self, request, *args, **kwargs):
        request.data["user"] = request.user.pk
        return super().create(request, *args, **kwargs)
