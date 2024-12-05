from django.db import models
from django.utils import timezone
from apps.users.models import User
from apps.inventory.models import Product
from apps.warehouses.models import Warehouse, WarehouseProduct, Item
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal
# Create your models here.



order_statuses = [
	('quote','Quote'),
	('hold','Hold'),
	('ready_to_pack','Ready To Pack'),
	('packed','Packed'),
	('on_site','On Site'),
	('returned','Returned'),
	('ready_to_invoice','Ready To Invoice'),
	('invoiced','Invoiced'),
	('paid','Paid'),
]


event_types = [
	('Personal','Personal'),
	('Business','Business'),
	('Familyk','Family'),
	('Holiday','Holiday'),
	('ETC','ETC'),
]

class Order(models.Model):
	client = models.ForeignKey("Client", on_delete=models.SET_NULL, null=True, blank=True)
	status = models.CharField(max_length=255, choices= order_statuses, default="quote")
	items = models.ManyToManyField('OrderItem', blank=True, related_name='order')
	order_date = models.DateField(default= timezone.now)
	event = models.ForeignKey('Event', on_delete=models.SET_NULL, null=True)
	labor = models.BooleanField(default=False)
	labor_details = models.TextField(null=True, blank=True)
	total_amount = models.FloatField(blank=True, null=True)
	primary_warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True, blank=True, related_name="booking_order_primary_warehouse+")
	scanned_items = models.ManyToManyField(Item, blank=True, related_name="order.scanned_items+")

	def get_order_items(self):
		return self.items.all()

	def get_order_scanned_items(self):
		return self.scanned_items.all()

	def __str__(self):
		try:
			event_name = self.event.first().name
		except:
			event_name = f'Order {self.id}'
		return (f'order for {event_name}')
	
	def change_to_hold(self):
		return reverse("change-to-hold", args=[self.id])


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
	country	= models.CharField(max_length=255, default="Canada")

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
	name = models.CharField(max_length=255)
	start = models.DateTimeField()
	end = models.DateTimeField()
	all_day = models.BooleanField(default=False)
	url = models.CharField(max_length=2047, null=True, blank=True)
	location = models.CharField(max_length=2047, null=True, blank=True)
	status = models.CharField(choices=order_statuses, default="quote", max_length=255, null=True, blank=True)
	description = models.CharField(max_length=1023, null=True, blank=True)
	event_type = models.CharField(max_length=1023, choices=event_types, default="ETC")
	project_type = models.CharField(choices=project_types, default='Dryhire', max_length=255)
	client = models.ForeignKey("Client", on_delete=models.SET_NULL, null=True, blank=True)
	url = models.CharField(max_length=2555, blank=True)
	event_manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	notes = models.TextField(blank=True, null=True)
	


	def get_url(self):
		return reverse("app-booking-detail", args=[self.id,])
	
	def get_edit_url(self):
		return reverse("app-booking-edit", args=[self.id,])
	
	def check_end(self):
		return self.end <= timezone.now()

	def __str__(self):
		return f"Event ({self.name}) - {self.start.strftime('%Y-%m-%d %H:%M')} to {self.end.strftime('%Y-%m-%d %H:%M')}"
	

class OrderItem(models.Model):
	w_product = models.ForeignKey(WarehouseProduct, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=1)
	custom_price = models.FloatField(
        validators=[MinValueValidator(0)],
        default=None,
        null=True,
        blank=True
    )

	def __str__(self):
		return (f'{self.w_product.product.name} - {self.quantity} pcs')
	
	def get_price(self):
		if self.custom_price is not None:
			return self.custom_price
		return self.w_product.product.rental_price

	def subtotal(self):
		return (self.get_price() * self.quantity)
	
	def check_item_availability(self):
		available_quantity = self.w_product.available_quantity()
		if available_quantity >= self.quantity:
			return True
		return False
	
	def get_remove_url(self):
		order = Order.objects.filter(items__in=[self]).first()
		return reverse("remove-quote-item", args=[self.id, order.id])

class PaymentAccount(models.Model):
	BANK_NAME = "Canada Bank"
	COUNTRY = "Canada"
	IBAN = "ETD95476213874685"
	SWIFT_CODE = "BR91905"

	bank_name = models.CharField(max_length=1000, default=BANK_NAME)
	country = models.CharField(max_length=1000, default=COUNTRY)
	iban = models.CharField(max_length=1000, default=IBAN)
	swift_code = models.CharField(max_length=1000, default=SWIFT_CODE)

class Invoice(models.Model):
	LANGUAGE_CHOICES = (
		('English', 'English'),
		('French', 'French'),
	)
	DUOSON_ADDRESS = "Office 149, 450 South Brand Brooklyn, San Diego County, CA 91905, USA"
	DUOSON_CONTACT = "+1 (123) 456 7891, +44 (876) 543 2198"
	
	duoson_address = models.CharField(max_length=1000, default=DUOSON_ADDRESS)
	duoson_contact = models.CharField(max_length=1000, default=DUOSON_CONTACT)
	order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='invoice')
	language = models.CharField(max_length=100, choices=LANGUAGE_CHOICES, default='English')
	issued_date = models.DateTimeField(default=timezone.now)
	due_date = models.DateField(null=True, blank=True)
	total_amount = models.FloatField(validators=[MinValueValidator(0)])
	is_paid = models.BooleanField(default=False)
	payment_date = models.DateField(null=True, blank=True)
	sales_person = models.CharField(max_length=100, null=True, blank=True)
	thanks_note = models.CharField(max_length=100, null=True, blank=True, default='Thanks for your business')
	note = models.CharField(max_length=1000, null=True, blank=True, default='It was a pleasure working with you and your team. We hope you will keep us in mind for future projects. Thank You!')
	discount = models.FloatField(validators=[MinValueValidator(0)], default=0.00)
	tax = models.FloatField(validators=[MinValueValidator(0)], default=0.00)
	payment_account = models.ForeignKey(PaymentAccount, on_delete=models.SET_NULL, null=True, blank=True)



	def __str__(self):
		return f"Invoice for Order {self.order.id}"

	def sub_total(self):
		subtotal = 0
		for item in self.order.items.all():
			subtotal += item.subtotal()
		return subtotal
	
	def total(self):
		self.sub_total - self.discount + self.tax

	def save(self, *args, **kwargs):
		if not self.payment_account:
			default_payment_account = PaymentAccount.objects.first()
			if not default_payment_account:
				default_payment_account = PaymentAccount.objects.create(
					bank_name=PaymentAccount.BANK_NAME,
					country=PaymentAccount.COUNTRY,
					iban=PaymentAccount.IBAN,
					swift_code=PaymentAccount.SWIFT_CODE
				)
			self.payment_account = default_payment_account
		self.total_amount = self.sub_total()  # Assuming sub_total is a method in your model

		super().save(*args, **kwargs)

# @receiver(post_save, sender=OrderItem)
# def update_invoice_total(sender, instance, **kwargs):
#     # Calculate the total amount for the invoice
#     total_amount = instance.order.invoice_set.aggregate(total=models.Sum('order__price.subtotal()'))['total'] or 0
#     instance.order.invoice_set.update(total=total_amount)