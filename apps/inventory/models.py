from django.db import models
from django.utils import timezone
from apps.users.models import User
from django.urls import reverse
from autoslug import AutoSlugField
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.

item_types = (
	("barcoded","Barcoded"),
	("non-barcoded","Non Barcoded"),
	)
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    manufacturer = models.CharField(max_length=255, blank=True, null=True)
    availability = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products/')
    rental_price = models.FloatField(blank=True, null=True, default=0.00)
    item_type= models.CharField(choices=item_types, max_length=20, default="barcoded")
    
    def __str__(self):
        return (f'{self.name} - {self.manufacturer}')
    
    def getdelete(self):
        return reverse('Product:product-delete', args=[self.id,])
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name

@receiver(pre_save, sender=Category)
def generate_category_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)

statuses = [
	("IN_HOUSE","In House"),
	("DEFECTIVE","Defective"),
	("MISSING","Missing"),
	("OKAY_RETURNED","Okay & Returned")
]

class LoanedProduct(models.Model):
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    status = models.CharField(choices=statuses, max_length=255,default='IN_HOUSE')
    loaned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    loaned_date = models.DateField(default= timezone.now)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.product.name

