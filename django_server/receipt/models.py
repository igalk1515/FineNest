from django.db import models
from django.utils.translation import gettext_lazy as _

class PaymentMethod(models.TextChoices):
    CASH = 'מזומן',
    CREDIT = 'אשראי',

class Receipt(models.Model):
    uid = models.CharField(max_length=255)
    business_name = models.CharField(max_length=255)
    receipt_number = models.CharField(max_length=100)
    total_price = models.CharField(max_length=50)
    payment_method = models.CharField(
        max_length=10,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CASH
    )
    credit_card_last_4_digits = models.CharField(max_length=4, blank=True, null=True)
    items = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)
