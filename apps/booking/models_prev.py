from django.db import models
from django.utils import timezone
from apps.users.models import User
from apps.inventory.models import Product
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator
from django.urls import reverse
# Create your models here.


order_statuses = [
	('Quote','Quote'),
	('Hold','Hold'),
	('Ready_to_pack','Ready To Pack'),
	('Packed','Packed'),
	('On_site','On Site'),
	('Returned','Returned'),
	('Ready_to_invoice','Ready To Invoice'),
	('Invoiced','Invoiced'),
	('Paid','Paid'),
]


event_types = [
	('Personal','Personal'),
	('Business','Business'),
	('Familyk','Family'),
	('Holiday','Holiday'),
	('ETC','ETC'),
]

class Order(models.Model):
	client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	status = models.CharField(max_length=255, choices= order_statuses, default="Quote")
	items = models.ManyToManyField('OrderItem', blank=True)
	order_date = models.DateField(default= timezone.now)
	event = models.ManyToManyField('Event', blank=True)
	labor = models.BooleanField(default=False)
	labor_details = models.TextField(null=True, blank=True)
	total_amount = models.FloatField(blank=True, null=True)

	def __str__(self):
		try:
			event_name = self.event.first().name
		except:
			event_name = f'Order {self.id}'
		return (f'order for {event_name}')


class Company(models.Model):
    name = models.CharField(max_length=255, blank=True)
    postal = models.CharField(max_length=10, blank=True)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255, default="United States")

    def __str__(self):
        return self.name.strip()

class Client(models.Model):
	title = models.CharField(max_length=255, blank=True)
	first_name = models.CharField(max_length=255)
	middle_name = models.CharField(max_length=255, blank=True)
	last_name = models.CharField(max_length=255)
	email = models.EmailField()
	mobile = PhoneNumberField(blank=True, null=True)
	phone = PhoneNumberField(blank=True, null=True)
	street = models.CharField(max_length=255)
	houseNo = models.CharField(max_length=255)
	postal = models.CharField(max_length=10, blank=True)
	state = models.CharField(max_length=255)
	country	= models.CharField(max_length=255, default="United States")

	company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='clients', null=True, blank=True)
	
	def __str__(self):
		name = f"{self.title} {self.first_name}" if self.title else self.first_name
		name += f" {self.middle_name} {self.last_name}" if self.middle_name else f" {self.last_name}"
		return name.strip()

	def get_address(self):
		address = f"{self.houseNo}, {self.street}, {self.state}, {self.country}"
		return address

	def getdelete(self):
		return reverse('client-delete', args=[self.id,])


project_types= [
('Dryhire', 'Dryhire'),
('Band', 'band'),
('Production', 'production')
]


class Event(models.Model):
	STATUS_CHOICES = [
        ('Canceled', 'Canceled'),
        ('Inquiry', 'Inquiry'),
        ('Concept', 'Concept'),
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Prepped', 'Prepped'),
        ('On Location', 'On Location'),
        ('Returned', 'Returned'),
    ]

	name = models.CharField(max_length=255)
	start = models.DateTimeField()
	end = models.DateTimeField()
	all_day = models.BooleanField(default=False)
	url = models.CharField(max_length=2047, null=True, blank=True)
	location = models.CharField(max_length=2047, null=True, blank=True)
	description = models.CharField(max_length=1023, null=True, blank=True)
	event_type = models.CharField(max_length=1023, choices=event_types, default="ETC")
	project_type = models.CharField(choices=project_types, default='Dryhire', max_length=255)
	client = models.ForeignKey("Client", on_delete=models.SET_NULL, null=True, blank=True)
	url = models.CharField(max_length=2555, blank=True)
	event_manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending', null=True)
	notes = models.TextField(blank=True, null=True)


	def get_url(self):
		return reverse("app-booking-detail", args=[self.id,])
	
	def __str__(self):
		return f"Event ({self.name}) - {self.start.strftime('%Y-%m-%d %H:%M')} to {self.end.strftime('%Y-%m-%d %H:%M')}"

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=1)
	custom_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=None,
        null=True,
        blank=True
    )

	def __str__(self):
		return (f'{self.product.name} - {self.quantity} pcs')
	
	def subtotal(self):
		if self.custom_price is not None:
			return self.custom_price * self.quantity
		else:
			return self.product.price * self.quantity


class Invoice(models.Model):
    LANGUAGE_CHOICES = (
        ('English', 'English'),
        ('French', 'French'),
    )

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='order_invoice')
    language = models.CharField(max_length=100, choices=LANGUAGE_CHOICES)
    issued_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    is_paid = models.BooleanField(default=False)
    payment_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Invoice for Order {self.order.id}"
