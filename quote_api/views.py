from .serializers import QuoteSerializer, UserSerializer
from .models import Quote
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView

class QuoteListCreateView(ListCreateAPIView):
    #all generics needs is serializer class and query set
    serializer_class = QuoteSerializer
    queryset = Quote.objects.all()

class QuoteRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = QuoteSerializer
    queryset = Quote.objects.all()

class RegistrationCreateView(CreateAPIView):
    serializer_class = UserSerializer
