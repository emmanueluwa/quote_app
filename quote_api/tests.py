from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status 
from .models import Quote
from rest_framework_api_key.models import APIKey

from .factories import QuoteFactory

class QuoteTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        #object, key
        api_key, key = APIKey.objects.create_key(name="quote-service")
        #authenticate everything with the key
        self.client.credentials(HTTP_AUTHORIZATION=f"Api-Key {key}")

    def test_create_quote(self):
        url = reverse("quote_api:quote-list-create")
        info = {
          "name": "Goku",
          "address": "QueensRoad",
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

    def test_list_quotes(self):
        quote = QuoteFactory()
        url = reverse("quote_api:quote-list-create")
        #using client, get quotes list
        response = self.client.get(url, format="json")

        #list wrapped in an array is returned
        json_response = response.json()

        #successful get status code should be 200
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        #get the objects within the array
        self.assertEqual(quote.name, json_response[0]["name"])
        self.assertEqual(quote.address, json_response[0]["address"])
        self.assertEqual(quote.description, json_response[0]["description"])

    def test_retrieve_expense(self):
        quote = QuoteFactory()
        #to retreive, update or delete an id is needed
        url = reverse("quote_api:quote-retrieve-update-destroy", args=[quote.id])

        response = self.client.get(url, format="json")
        json_response = response.json()

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(quote.name,json_response["name"])
        self.assertEqual(quote.address, json_response["address"])
        self.assertEqual(quote.description, json_response["description"])

    def test_delete_quote(self):
        quote = QuoteFactory()

        url = reverse("quote_api:quote-retrieve-update-destroy", args=[quote.id])

        #delete whatever is in the url
        response = self.client.delete(url, format="json")

        #assert there is no content and that record no longer exists
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertFalse(Quote.objects.filter(id=quote.id))

    def test_update_quote(self):
        #random record from factory
        quote = QuoteFactory()

        url = reverse("quote_api:quote-retrieve-update-destroy", args=[quote.id])
        info = {
            "name": "OhSo",
            "address": "GreatnessLane",
        }

        response = self.client.put(url, info, format="json")

        #db fetch updated info
        updated_quote = Quote.objects.get(id=quote.id)
        
        #checking updated info matches info added
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(updated_quote.name, info["name"])
        self.assertEqual(updated_quote.address, info["address"])
    
    def test_unsuccessful_quote_update(self):
        quote = QuoteFactory()

        url = reverse("quote_api:quote-retrieve-update-destroy", args=[quote.id])
        info = {
            
        }

        response = self.client.put(url, info, format="json")
        json_response = response.json()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        #response from serializer when required fields are not filled
        self.assertEqual(json_response["name"], ["This field is required."])
        self.assertEqual(json_response["address"], ["This field is required."])

