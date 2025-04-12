from django.urls import path
from .views import upload_receipt

urlpatterns = [
    path('receipt/', upload_receipt, name='upload_receipt'),
]
