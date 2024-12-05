from django.db import models
from apps.inventory.models import *
from autoslug import AutoSlugField
from django.db.models import Sum, Count, Q


class Warehouse(models.Model):
	name = models.CharField(max_length=255, unique=True)
	slug = AutoSlugField(populate_from='name')
	location = models.CharField(max_length=255, null=True, blank=True)
	products = models.ManyToManyField('WarehouseProduct', blank=True, related_name='warehouses')
	contact_person = models.CharField(max_length=255, null=True, blank=True)
	contact_email = models.CharField(max_length=255, null=True, blank=True)
	contact_phone = models.CharField(max_length=255, null=True, blank=True)

	def stock_quantity(self):
		return self.products.all().aggregate(total_items=Count('items'))['total_items'] or 0

	def available_quantity(self):
		return self.products.all().aggregate(total_available_items=Count('items', filter=Q(items__status='available')))['total_available_items'] or 0

	def damaged_quantity(self):
		return self.products.all().aggregate(total_available_items=Count('items', filter=Q(items__status='damaged')))['total_available_items'] or 0

	def reserved_quantity(self):
		return self.products.all().aggregate(total_available_items=Count('items', filter=Q(items__status='reserved')))['total_available_items'] or 0

	def __str__(self):
		return self.name + " Warehouse"

class WarehouseProduct(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	items = models.ManyToManyField("Item", blank=True)

	def stock_quantity(self):
		return (self.items.count())

	def available_quantity(self):
		return (self.items.filter(status="available").count())

	def damaged_quantity(self):
		return (self.items.filter(status="damaged").count())

	def reserved_quantity(self):
		return (self.items.filter(status="reserved").count())

	def getslug(self):
		return (self.product.name + "-"+str(self.id))
	
	def __str__(self):
		return self.product.name

	def get_available(self):
		return (self.items.filter(status="available").count())

item_statuses = (
	("available","Available"),
	("damaged","Damaged"),
	("reserved","Reserved")
	)


class Item(models.Model):
	barcode = models.CharField(max_length=20, unique=True, null=True, blank=True)
	status = models.CharField(choices=item_statuses, default="available", max_length=9)
	purchase_date = models.DateField(default= timezone.now)
	purchase_price = models.FloatField(blank=True, null=True)
	count = models.IntegerField(null=True)
	unavailable = models.IntegerField(default=0)
	

	def get_product(self):
		wareproduct = WarehouseProduct.objects.get(items=self)
		return(wareproduct.product)
	
	def __str__(self):
		wareproduct = WarehouseProduct.objects.get(items=self)
		warehouse = Warehouse.objects.get(products=wareproduct)
		ret = ""
		if(self.barcode):
			ret += f'barcode: {self.barcode} - '
		ret += f'{wareproduct.product.name} - {warehouse.name}'
		return ret
	
	def str_no_warehouse(self):
		wareproduct = WarehouseProduct.objects.get(items=self)
		ret = ""
		if(self.barcode):
			ret += f'barcode: {self.barcode} - '
		ret += f'{wareproduct.product.name}'
		return ret

	def get_available(self):
		return(self.count-self.unavailable)
	


trans_stats = (
	("pending","Pending"),
	("transferred","Transferred"),
	("rejected","Rejected")
	)

trans_types = (
	("single","Single"),
	("multiple","Multiple"),
	)
class Transfer(models.Model):
	fro = models.ForeignKey(Warehouse, verbose_name="from", on_delete=models.SET_NULL, null=True, related_name="from+")
	to = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True)
	time = models.DateTimeField(default=timezone.now)
	item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True)
	count = models.IntegerField(default=1)
	status = models.CharField(max_length=20, choices = trans_stats, default="pending")
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
	trans_type = models.CharField(choices=trans_types, default="single", max_length=255)
	items = models.ManyToManyField(Item, blank=True, related_name="transfer.items+")


	def make_transfer(self):
		try:
			if(self.trans_type == "single"):
				wareproduct = WarehouseProduct.objects.get(items=self.item)
				source_warehouse = Warehouse.objects.get(products=wareproduct)
			else:
				source_warehouse = self.fro
				wareproduct = source_warehouse.products.filter(product=self.product).first()
				if(not wareproduct):
					wareproduct = WarehouseProduct(product=self.product)
					wareproduct.save()
					source_warehouse.product.add(wareproduct)
					source_warehouse.save()
			if(source_warehouse == self.to and wareproduct.product.item_type == "barcoded" and self.trans_type=="single"):
				return ("Item not found in warehouse!")
			if (source_warehouse != self.to or wareproduct.product.item_type == "non-barcoded"):
				nwwareproduct, created = self.to.products.get_or_create(product=wareproduct.product)
				if(wareproduct.product.item_type== "barcoded"):
					if(self.trans_type == "single"):
						nwwareproduct.items.add(self.item)
						wareproduct.items.remove(self.item)
					else:
						if not self.items.all().count():
							return ("No item selected!")
						for item in self.items.all():
							if(item.status != "available"):
								self.items.remove(item)
							else:
								fwareproduct = WarehouseProduct.objects.filter(items__in=[item]).first()
								if(fwareproduct not in self.fro.products.all()):
									self.items.remove(item)
						self.save()
						for item in self.items.all():
							nwwareproduct.items.add(item)
							wareproduct.items.remove(item)
					self.status = "transferred"
					self.time = timezone.now()
					self.save()
					return(self.status)
				else:
					wid = wareproduct.product.id
					oldwp = self.fro.products.filter(product__id=wid).first()
					olditem = oldwp.items.first()
					if(olditem.get_available() < self.count):
						return ("not enough items")
					if(nwwareproduct.items.all().count() ==0):
						nwitem = Item(purchase_date=self.item.purchase_date, purchase_price=self.item.purchase_price, count=self.count)
						nwitem.save()
						nwwareproduct.items.add(nwitem)
						nwwareproduct.save()
						self.to.products.add(nwwareproduct)
						self.to.save()
					else:
						nwitem =nwwareproduct.items.first()
						nwitem.count +=self.count
						nwitem.save()
					nwwareproduct.save()
					olditem.count -= self.count
					olditem.save()
					self.status = "transferred"
					self.time = timezone.now()
					self.save()
					return(self.status)

		except (WarehouseProduct.DoesNotExist, Warehouse.DoesNotExist) as e:
			return ("Product does not exist in warehouse")
	

	def unmake_transfer(self):
		self.status = "rejected"
		self.time = timezone.now()
		self.save()
		return(self.status)
		


	def get_item(self):
		wareproduct = WarehouseProduct.objects.get(items=self.item)
		if(wareproduct.product.item_type =="barcoded"):
			if(self.trans_type == "single"):
				return(self.item.str_no_warehouse())
			else:
				ret =""
				if(self.count):
					ret = f'({self.count}) '
				return (ret + self.product.name)
		else:
			return(f'({self.count}) {self.item.str_no_warehouse()}')

	def __str__(self):
		return self.get_item()