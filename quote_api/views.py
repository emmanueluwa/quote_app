from django.shortcuts import get_object_or_404
from .serializers import QuoteSerializer, UserSerializer
from .models import Quote
from django.contrib.auth.models import User
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework import exceptions, status
from rest_framework.response import Response
from quote_api.authentication import generate_access_token, JWTAuthentication
from rest_framework.permissions import IsAuthenticated

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

class SessionRetrieveDestroyView(APIView):
    #we need an authentication class and permission class
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        #the user attached jwt authentication, is attached to the request. serializer cleans data
        serializer = UserSerializer(request.user)
        return Response({"data": serializer.data})

    def delete(self, request):
        #first create response to be able to delete cookie
        response = Response()
        response.delete_cookie(key='jwt')
        response.data = {'message': "Logged out"}

        return response
