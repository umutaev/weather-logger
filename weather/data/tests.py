from datetime import datetime, timezone
from typing import List
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
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


class DataCreateTestCase(APITestCase):
    url = reverse("list_data")

    def setUp(self):
        UserModel = get_user_model()
        user = UserModel.objects.create(username="test")
        token = Token.objects.create(user=user)
        self.token = token.key

    def test_creation(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        response = self.client.post(
            self.url,
            {
                "temperature": [{"value": 10, "label": "outside"}],
                "humidity": [{"value": 50, "label": "outside"}],
                "pressure": [{"value": 900}],
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Gather record object from the database
        record = DatarecordModel.objects.get(pk=response.data["id"])
        # Gather all temperature records tied with that record
        temperature = TemperatureModel.objects.filter(record=record).all()
        self.assertEqual(temperature.__len__(), 1)
        temperature = temperature[0]
        # Gather all pressure records tied with that record
        pressure = PressureModel.objects.filter(record=record).all()
        self.assertEqual(pressure.__len__(), 1)
        pressure = pressure[0]
        # Gather all humidity records tied with that record
        humidity = HumidityModel.objects.filter(record=record).all()
        self.assertEqual(humidity.__len__(), 1)
        humidity = humidity[0]

        # New request
        self.client.credentials()
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.data.__len__(), 1)
        # fmt: off
        self.assertEqual(response.data[0]["temperature"].__len__(), 1)
        self.assertEqual(response.data[0]["temperature"][0]["value"], temperature.value)
        self.assertEqual(response.data[0]["temperature"][0]["label"], temperature.label)
        self.assertEqual(response.data[0]["humidity"].__len__(), 1)
        self.assertEqual(response.data[0]["humidity"][0]["value"], humidity.value)
        self.assertEqual(response.data[0]["humidity"][0]["label"], humidity.label)
        self.assertEqual(response.data[0]["pressure"].__len__(), 1)
        self.assertEqual(response.data[0]["pressure"][0]["value"], pressure.value)
        self.assertEqual(response.data[0]["pressure"][0]["label"], pressure.label)
        self.assertEqual(
            datetime.fromisoformat(response.data[0]["creation_date"].replace("Z", "+00:00")),
            record.creation_date,
        )
        self.assertEqual(response.data[0]["user"], record.user.id)
        # fmt: on
