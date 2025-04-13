from django.urls import path
from .views import upload_receipt, create_receipt, get_all_receipts

urlpatterns = [
    path('receipt/upload/', upload_receipt, name='upload_receipt'),
    path('receipt/create/', create_receipt, name='create_receipt'),
    path('receipt/all/', get_all_receipts, name='get_all_receipts'),
]
