from django.db import models

class Receipt(models.Model):
    uid = models.CharField(max_length=255)
    business_name = models.CharField(max_length=255)
    receipt_number = models.CharField(max_length=100)
    total_price = models.CharField(max_length=50)
    payment_method = models.CharField(max_length=100)
    credit_card_last_4_digits = models.CharField(max_length=4, blank=True, null=True)
    items = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)
