from django.urls import path
from data.views import DataView

urlpatterns = [path("", DataView.as_view(), name="list_data")]
