from django.urls import path
from . import views

urlpatterns = [
    path("quotes/", views.QuoteListCreateView.as_view(), name="quote-list-create")
]
