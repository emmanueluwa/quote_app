from rest_framework import status 
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import QuoteSerializer
from .models import Quote
from django.shortcuts import get_object_or_404

class QuoteListCreateView(APIView):
    def post(self, request):
        #use serializer to make data a json object
        serializer = QuoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            #only one response is returned
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        quotes = Quote.objects.all()
        serializer = QuoteSerializer(quotes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class QuoteRetrieveUpdateDestroyView(APIView):
    #get method
    def get(self, request, pk):
        quote = get_object_or_404(Quote, pk=pk)
        serializer = QuoteSerializer(quote, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

