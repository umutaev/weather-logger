from datetime import datetime, timezone
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from data.models import DatarecordModel, TemperatureModel, HumidityModel, PressureModel


class DataGatherTestCase(APITestCase):
    url = reverse("list_data")

    def setUp(self):
        UserModel = get_user_model()
        UserModel.objects.create(username="test1")
        UserModel.objects.create(username="test2")

    def test_empty_gather(self):
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_gather(self):
        user = get_user_model().objects.filter(username="test1").get()
        record = DatarecordModel.objects.create(user=user)
        temperature = TemperatureModel.objects.create(value=12, record=record)
        humidity = HumidityModel.objects.create(value=50, record=record)
        pressure = PressureModel.objects.create(value=900, record=record)
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.data.__len__(), 1)
        self.assertEqual(response.data[0]["id"], record.id)
        self.assertEqual(response.data[0]["temperature"].__len__(), 1)
        self.assertEqual(response.data[0]["temperature"][0]["value"], temperature.value)
        self.assertEqual(response.data[0]["humidity"].__len__(), 1)
        self.assertEqual(response.data[0]["humidity"][0]["value"], humidity.value)
        self.assertEqual(response.data[0]["pressure"].__len__(), 1)
        self.assertEqual(response.data[0]["pressure"][0]["value"], pressure.value)
        self.assertEqual(
            datetime.fromisoformat(
                response.data[0]["creation_date"].replace("Z", "+00:00")
            ),
            record.creation_date,
        )
        self.assertEqual(response.data[0]["user"], user.id)
