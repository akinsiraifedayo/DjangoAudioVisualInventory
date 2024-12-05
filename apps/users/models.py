from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.urls import reverse
from django.utils import timezone
from apps.roles.models import Role

# Create your models here.

class User(AbstractUser):
	Profile_pic = models.ImageField(upload_to='profile/pictures', null=True, blank=True)
	first_name = models.CharField(max_length=20, null=True, blank=True)
	last_name = models.CharField(max_length=20, null=True, blank=True)
	is_salesperson = models.BooleanField(default=False)
	is_operations_manager = models.BooleanField(default=False)
	is_equipment_manager = models.BooleanField(default=False)
	is_warehouse_staff = models.BooleanField(default=False)
	is_technician = models.BooleanField(default=False)
	is_account_manager = models.BooleanField(default=False)
	is_account_department = models.BooleanField(default=False)
	Gender = models.CharField(max_length=6, null=True, blank=True)
	Phone_number = models.CharField(max_length=20, null=True, blank=True)
	Feeds = models.ManyToManyField('Feed',blank=True)
	staff_id =models.CharField(max_length=255, null=True, blank=True)
	roles = models.ManyToManyField(Role, blank=True)

	def get_name(self):
		name_parts = [part for part in [self.first_name, self.last_name] if part]
		return ' '.join(name_parts)

	def get_url(self):
		url = reverse("accountView", args=[self.id,])
		return (url)

	def get_status(self):
		if(self.is_active):
			return ("Active")
		else:
			return ("Inactive")

	def get_fake_status(self):
		if(self.is_active):
			return (2)
		else:
			return (3)

	def get_roles(self):
		roles =""
		for role in self.roles.all():
			roles += role.name + " "
		if(roles == ""):
			roles = "Not Assigned"
		return roles

ftypes = [
	('savings','savings'),
	('investment','investment'),
	('loan','loan'),
	('target','target'),
]


class Feed(models.Model):
    body = models.CharField(max_length=255)
    read = models.BooleanField(default=False)
    time = models.DateTimeField(default=timezone.now)
    ftype = models.CharField(max_length=255, choices=ftypes, default='savings')

    def gettime(self):
    	if(self.time.date() == timezone.now().date()):
    		return (self.time.strftime("%H:%M %p"))
    	else:
    		return (self.time.strftime("%H:%M %p %d/%m/%Y"))
    def getstatus(self):
    	if(self.read == False):
    		return ('false')
    	else:
    		return ('true')


