from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status 
from .models import Quote
import jwt
from django.conf import settings

from .factories import QuoteFactory, UserFactory

class QuoteTests(TestCase):
    def setUp(self):
        self.client = APIClient()

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


class RegisterTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("quote_api:registration-create")

    def test_registration(self):
        info = {
            "email": "wisest@mail.com",
            "password": "pass123",
            "username": "wise1"
        }
        response = self.client.post(self.url, info, format="json")
        json_response = response.json()

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(json_response["email"], info["email"])
        self.assertEqual(json_response["username"], info["username"])
        # confirming password is not sent back w response
        with self.assertRaises(KeyError):
            json_response["password"]


class SessionCreateTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("quote_api:session-create")
        #password stated here incase it is changed in factories
        self.user = UserFactory(password='password123')

    def test_create_session(self):
        #password above is hashed so we state it unhashed below
        info = {"username": self.user.username, "password": "password123"}

        response = self.client.post(self.url, info, format="json")

        #decode the data using the algorithm and secret key
        decoded_token = jwt.decode(
            response.data["jwt"], settings.SECRET_KEY, algorithms=["HS256"]
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue("jwt" in response.data)
        self.assertEqual(self.user.id, decoded_token["user_id"])


class SessionRetrieveDestroyTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory(password="password123")

    def test_retrieve_session(self):
        #using a non hashed password
        info = {"username": self.user.username, "password": "password123"}
        #creating session
        self.client.post(reverse("quote_api:session-create"), info, format="json")

        #process of retrieving session
        response = self.client.get(
            reverse("quote_api:session-retrieve-destroy"), format="json"
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data["data"]["id"], self.user.id)
        self.assertEqual(response.data["data"]["email"], self.user.email)
