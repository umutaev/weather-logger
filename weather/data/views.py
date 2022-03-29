from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters import rest_framework as filters
from data.models import DatarecordModel, TemperatureModel, HumidityModel, PressureModel
from data.serializers import (
    DatarecordSerializer,
    TemperatureSerializer,
    HumiditySerializer,
    PressureSerializer,
)


class DataFilterset(filters.FilterSet):
    creation_date = filters.IsoDateTimeFromToRangeFilter()

    class Meta:
        model = DatarecordModel
        fields = [
            "user",
            "temperature__label",
            "humidity__label",
            "pressure__label",
            "creation_date",
        ]


class DataView(ListAPIView, CreateAPIView):
    queryset = DatarecordModel.objects.all().prefetch_related(
        "temperature", "humidity", "pressure"
    )
    permissions_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = DatarecordSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = DataFilterset

    def create(self, request, *args, **kwargs):
        request.data["user"] = request.user.pk
        return super().create(request, *args, **kwargs)
