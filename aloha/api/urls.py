from django.urls import path
from .views import (
    clientsView, 
    ProviderView,
)

urlpatterns = [
 

    path('clients/', clientsView.as_view(), name='clients'),
    path('clients/<str:Alias>/', clientsView.as_view(), name='client-by-alias'),
    path('Provider/', ProviderView.as_view(), name='Provider'),  # Define the URL for the Users view
]
 