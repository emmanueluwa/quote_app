from django.shortcuts import get_object_or_404
from .serializers import QuoteSerializer, UserSerializer
from .models import Quote
from django.contrib.auth.models import User
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework import exceptions, status
from rest_framework.response import Response
from quote_api.authentication import generate_access_token

class QuoteListCreateView(ListCreateAPIView):
    #all generics needs is serializer class and query set
    serializer_class = QuoteSerializer
    queryset = Quote.objects.all()

class QuoteRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = QuoteSerializer
    queryset = Quote.objects.all()

class RegistrationCreateView(CreateAPIView):
    serializer_class = UserSerializer

class SessionCreateView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = get_object_or_404(User, username=username)   

        #check user found matches password given
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed(
                "Incorrect Password", code=status.HTTP_401_UNAUTHORIZED
            )
        
        #generate access token using logged in username and password as token
        token = generate_access_token(user)

        response = Response()
        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = {"jwt": token}

        return response
