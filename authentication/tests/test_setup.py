from rest_framework.test import APITestCase
from django.urls import reverse
from faker import Faker

from authentication.models import User


class TestSetUp(APITestCase):
    def setUp(self):
        self.register_url = reverse("authentication:register")
        self.login_url = reverse("authentication:login")
        self.fake = Faker()

        self.user_data = {
            "email": self.fake.email(),
            "first_name": self.fake.name(),
            "last_name": self.fake.name(),
            "username": self.fake.email().split("@")[0],
            "password": self.fake.email(),
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
