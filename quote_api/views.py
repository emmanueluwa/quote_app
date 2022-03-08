from .serializers import QuoteSerializer
from .models import Quote
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_api_key.permissions import HasAPIKey

class QuoteListCreateView(ListCreateAPIView):
    #all generics needs is serializer class and query set
    serializer_class = QuoteSerializer
    queryset = Quote.objects.all()
    permission_classes = [HasAPIKey]

class QuoteRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = QuoteSerializer
    queryset = Quote.objects.all()
    permission_classes = [HasAPIKey]

