from django.urls import path
from .views import (
    clientsView, 
    ProviderView,
)

urlpatterns = [
    # Patients API
    path('clients/', clientsView.as_view(), name='clients'),  # Handles GET, POST, PUT, DELETE
    
   
    path('Provider/', ProviderView.as_view(), name='Provider'),  # Define the URL for the Users view
]
 
