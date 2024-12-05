from django.db import models
from django.utils import timezone
from apps.users.models import User
from apps.inventory.models import Product
from apps.booking.models import Order
# Create your models here.



languages = [
	('EN','English'),
	('FR','French'),
]

class Invoice(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='sale.invoice.invoiceorder+')
	language = models.CharField(max_length=255, choices=languages, default='EN')
	issued_date = models.DateField(default=timezone.now)
	due_date = models.DateField(null=True, blank=True)
	total_amount = models.FloatField(blank=True, null=True)
	is_paid = models.BooleanField(default=False)
	payment_date = models.DateField(blank=True, null=True)


