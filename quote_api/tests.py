from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status 

class QuoteTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_quote(self):
        url = reverse("quote_api:quote-list-create")
        info = {
          "name": "Goku",
          "address": "Queens Road",
        }

        response = self.client.post(url, info, format="json")
        #changing to json object
        json_response = response.json()

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        # checking address is the same as manual input address
        self.assertEqual(info["name"], json_response["name"])
        self.assertEqual(info["address"], json_response["address"])
        #checking id is created along with the new record in database
        self.assertIsInstance(json_response["id"], int)


