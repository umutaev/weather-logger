from datetime import datetime
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from data.models import DatarecordModel


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
        record = DatarecordModel.objects.create(
            user=user, value=12, type=DatarecordModel.RecordType.TEMPERATURE
        )
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.data.__len__(), 1)
        self.assertEqual(response.data[0]["id"], record.id)
        self.assertEqual(response.data[0]["value"], record.value)
        self.assertEqual(response.data[0]["type"], record.type)
        self.assertEqual(
            datetime.fromisoformat(
                response.data[0]["creation_date"].replace("Z", "+00:00")
            ),
            record.creation_date,
        )
        self.assertEqual(
            datetime.fromisoformat(response.data[0]["date"].replace("Z", "+00:00")),
            record.date,
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
            {"value": 12, "type": "TEMPERATURE"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Gather record object from the database
        record = DatarecordModel.objects.get(pk=response.data["id"])

        # New request
        self.client.credentials()
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.data.__len__(), 1)
        self.assertEqual(response.data[0]["id"], record.id)
        self.assertEqual(response.data[0]["value"], record.value)
        self.assertEqual(response.data[0]["type"], record.type)
        self.assertEqual(
            datetime.fromisoformat(
                response.data[0]["creation_date"].replace("Z", "+00:00")
            ),
            record.creation_date,
        )
        self.assertEqual(
            datetime.fromisoformat(response.data[0]["date"].replace("Z", "+00:00")),
            record.date,
        )
        self.assertEqual(response.data[0]["user"], record.user.id)
