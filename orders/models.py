from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

# Create your models here.
class Customer(models.Model):
	user=models.OneToOneField(User, on_delete=models.CASCADE)
	name=models.CharField(max_length=32)

	def __str__(self):
		return f"Customer name - {self.name}"

class Topping(models.Model):
	topping_name=models.CharField(max_length=16)

	def __str__(self):
		return f"{self.topping_name}"

class Pizza(models.Model):
	pizza_name=models.CharField(max_length=32)
	topping_type=models.CharField(max_length=16)
	size=models.CharField(max_length=16)
	price=models.IntegerField()

	def __str__(self):
		return f"{self.pizza_name} with {self.topping_type} - {self.size} size of Rs.{self.price}"

class Sub(models.Model):
	sub_name=models.CharField(max_length=32)
	size=models.CharField(max_length=16)
	price=models.IntegerField()

	def __str__(self):
		return f"{self.sub_name} Sub - {self.size} size of Rs.{self.price}"

class Cart(models.Model):
	cust_id=models.ForeignKey(Customer, on_delete=models.CASCADE)
	@property
	def count(self):
		return Cart_Item.objects.filter(cart=self).aggregate(Sum('quantity'))['quantity__sum']
	@property
	def total(self):
		items=Cart_Item.objects.filter(cart=self)
		t=0
		for o in items:
			if(o.pizza):
				t+=o.pizza.price*o.quantity
			elif(o.sub):
				t+=o.sub.price*o.quantity
		return t
	
	
	# count=models.IntegerField(default=0)
	# total=models.IntegerField(default=0)

	def __str__(self):
		return f"{self.cust_id} Cart - {self.count} items - Total= Rs.{self.total}"

class Cart_Item(models.Model):
	pizza=models.ForeignKey(Pizza, blank=True, null=True, on_delete=models.CASCADE)
	toppings=models.ManyToManyField(Topping, blank=True)
	sub=models.ForeignKey(Sub, blank=True, null=True, on_delete=models.CASCADE)
	quantity=models.IntegerField()
	cart=models.ForeignKey(Cart, on_delete=models.CASCADE)

	def __str__(self):
		top=", ".join(str(i) for i in self.toppings.all())
		if(self.sub is None):
			return f"{self.pizza} - {top} - Quantity={self.quantity}"
		else:
			return f"{self.sub} - Quantity={self.quantity}"

class Order(models.Model):
	cust_id=models.ForeignKey(Customer, on_delete=models.CASCADE)
	@property
	def count(self):
		return Order_Item.objects.filter(order=self).aggregate(Sum('quantity'))['quantity__sum']
	@property
	def total(self):
		items=Order_Item.objects.filter(order=self)
		t=0
		for o in items:
			if(o.pizza):
				t+=o.pizza.price*o.quantity
			elif(o.sub):
				t+=o.sub.price*o.quantity
		return t

	def __str__(self):
		return f"{self.cust_id} Order - {self.count} items - Total= Rs.{self.total}"

class Order_Item(models.Model):
	pizza=models.ForeignKey(Pizza, blank=True, null=True, on_delete=models.CASCADE)
	toppings=models.ManyToManyField(Topping, blank=True)
	sub=models.ForeignKey(Sub, blank=True, null=True, on_delete=models.CASCADE)
	quantity=models.IntegerField()
	order=models.ForeignKey(Order, on_delete=models.CASCADE, related_name="o_items")

	def __str__(self):
		top=", ".join(str(i) for i in self.toppings.all())
		if(self.sub is None):
			return f"{self.pizza} - {top} - Quantity={self.quantity}"
		else:
			return f"{self.sub} - Quantity={self.quantity}"