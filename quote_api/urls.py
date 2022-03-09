from django.urls import path
from . import views

urlpatterns = [
    path("quotes/", views.QuoteListCreateView.as_view(), name="quote-list-create"),
    path("quotes/<str:pk>", views.QuoteRetrieveUpdateDestroyView.as_view(), name="quote-retrieve-update-destroy"),
    path("registrations/", views.RegistrationCreateView.as_view(), name="registration-create"),
    path("sessions/", views.SessionCreateView.as_view(), name="session-create")
]
