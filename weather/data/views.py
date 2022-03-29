from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters import rest_framework as filters
from data.models import DatarecordModel
from data.serializers import DatarecordSerializer


class DataFilterset(filters.FilterSet):
    date = filters.IsoDateTimeFromToRangeFilter()
    user = filters.BaseInFilter()
    label = filters.BaseInFilter()
    type = filters.BaseInFilter()

    class Meta:
        model = DatarecordModel
        fields = ["user", "type", "label"]


class DataView(ListAPIView, CreateAPIView):
    queryset = DatarecordModel.objects.all()
    permissions_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = DatarecordSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = DataFilterset

    def create(self, request, *args, **kwargs):
        request.data["user"] = request.user.pk
        return super().create(request, *args, **kwargs)
