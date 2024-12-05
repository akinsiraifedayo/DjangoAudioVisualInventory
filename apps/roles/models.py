from django.db import models

# Create your models here.

class Role(models.Model):
	name = models.CharField(max_length=100, blank=True, verbose_name='name')
	usermanage = models.BooleanField(default=False, verbose_name='User Management')
	clientmanage = models.BooleanField(default=False, verbose_name='Client Management')
	rolmanage = models.BooleanField(default=False, verbose_name='Role Management')
	commanage = models.BooleanField(default=False, verbose_name='Company Management')
	warmanage = models.BooleanField(default=False, verbose_name='Warehouse Management')
	evemanage = models.BooleanField(default=False, verbose_name='Event Management')
	promanage = models.BooleanField(default=False, verbose_name='Product Management')
	docmanage = models.BooleanField(default=False, verbose_name='Document Management')
	invmanage = models.BooleanField(default=False, verbose_name='Invoice Management')
	description = models.TextField(blank=True, verbose_name='description')


	def __str__(self):
		return (self.name)


	def getrole(self):
		result = list()
		fields =[f.name for f in Role._meta.get_fields()]
		del fields[0]
		values = list()
		names = list()
		for f in fields:
			names.append(Role._meta.get_field(f).verbose_name)
		for f in fields:
			values.append(getattr(self, f))
		count = len(fields)
		a = 0
		while (a < count):
			result.append({'name':fields[a],'value':values[a],'des':names[a]})
			a+=1
		return(result)

	def getstaff(self):
		uses = User.objects.filter(role=self).count()
		return({self.name:uses})

	@classmethod
	def get_field_descriptions(cls):
		return {
			'usermanage': 'Create/Edit/Delete Users: Allows managing user accounts within the system, view User Profiles: Grants access to view user details and profiles, enables assigning roles and permissions to other users.',
			'clientmanage': ' Allows managing client accounts, including contact information and preferences, grants access to view detailed profiles and history of clients, enables assigning clients to specific users or account managers for personalized service.',
			'rolmanage': 'Allows defining custom roles with specific sets of permissions., grants the ability to assign predefined roles to users based on their responsibilities., implements RBAC to control access to system functionalities based on user roles.',
			'commanage': 'Add/Edit/Delete Companies: Allows managing company accounts, including company details and contacts, grants access to view detailed profiles and history of companies, enables associating clients with their respective companies for organizational purposes.',
			'warmanage': 'Track Inventory Levels: Allows monitoring the stock levels of musical equipment, enables managing physical locations and storage areas, allows handling the receiving and shipping of products.',
			'evemanage': 'Schedule/Manage Events: Allows creating and managing events related to equipment rentals, grants access to view a calendar with scheduled events, enables managing registrations and attendees for events.',
			'promanage': 'Add/Edit/Delete Products: Allows managing the inventory of musical equipment, grants access to view detailed information about products, enables creating and managing categories for products.',
			'docmanage': 'Allows users to upload, edit, and delete documents related to rentals, agreements, or equipment specifications, grants access to a centralized repository of documents for easy retrieval and sharing, enables version control for documents to track changes and revisions.',
			'invmanage': 'Create/Edit/Delete Invoices: Allows creating, editing, and deleting invoices for rentals, view Invoice History: Grants access to view past invoices and rental history, enables recording payments and managing payment details.',
		}




