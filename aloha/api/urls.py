from django.urls import path
from .views import (
    clientsView, 
    ProviderView,
)

urlpatterns = [
 

    path('clients/', clientsView.as_view(), name='clients'),
   
    path('Provider/', ProviderView.as_view(), name='Provider'),  # Define the URL for the Users view
]
 