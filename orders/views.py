from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt
from .models import Customer, Pizza, Sub, Cart, Cart_Item, Topping, Order, Order_Item

# Create your views here.
# view which handles login
def index(request):
	try:
		u_name=request.POST["u_name"]
		password=request.POST["password"]
		u=authenticate(request, username=u_name, password=password)
		if(u is not None):
			login(request, u)
			return HttpResponseRedirect(reverse('profile'))
		else:
			messages.add_message(request, messages.WARNING, "Invalid credentials")
			return render(request, "orders/login.html")
	except:
		if(not request.user.is_authenticated):
			return render(request, "orders/login.html")
		else:
			return HttpResponseRedirect(reverse('profile'))

# view which handles registration
def register(request):
	try:
		u_name=request.POST["u_name"]
		name=request.POST["name"]
		email=request.POST["email"]
		password=request.POST["password"]
		u=User.objects.create_user(username=u_name, email=email, password=password)
		u.save()
		c=Customer(user=u, name=name)
		c.save()
		messages.add_message(request, messages.INFO, "Succesfully registered")
		return HttpResponseRedirect(reverse('index'))
	except:
		return render(request, "orders/register.html")

# view rendered on login aka profile page
def profile(request):
	return render(request, "orders/profile.html")

# view rendered on logout
def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))

# view which manages pizzas section
def pizzas(request):
	u=request.user
	cart,created=Cart.objects.get_or_create(cust_id=u.customer)
	context={
		"pizzas": Pizza.objects.all(),
		"toppings": Topping.objects.all()
	}
	if(request.POST):
		pizza_id=request.POST["pizza_id"]
		p=Pizza.objects.get(id=pizza_id)
		quantity=request.POST["quantity"]
		all_toppings=[]
		# cart.count+=int(quantity)
		# cart.total+=int(quantity)*p.price
		# cart.save()
		if(request.POST.get("topping1",False)):
			all_toppings.append(request.POST["topping1"])
			# topping1=request.POST["topping1"]
			# item.toppings.add(topping1)
			# item.save()
			if(request.POST.get("topping2",False)):
				all_toppings.append(request.POST["topping2"])
				# topping2=request.POST["topping2"]
				# item.toppings.add(topping2)
				# item.save()
				if(request.POST.get("topping3",False)):
					all_toppings.append(request.POST["topping3"])
					# topping3=request.POST["topping3"]
					# item.toppings.add(topping3)
					# item.save()
		try:
			if(len(all_toppings)==1):
				ordered_pizza=Cart_Item.objects.filter(pizza=p, cart=cart).annotate(num_toppings=Count('toppings')).get(toppings__in=all_toppings[0], num_toppings__exact=1)
			elif(len(all_toppings)==2):
				ordered_pizza=Cart_Item.objects.filter(pizza=p, cart=cart).annotate(num_toppings=Count('toppings')).filter(toppings__in=all_toppings[0], num_toppings__exact=2).get(toppings__in=all_toppings[1], num_toppings__exact=2)
			elif(len(all_toppings)==3):
				ordered_pizza=Cart_Item.objects.filter(pizza=p, cart=cart).annotate(num_toppings=Count('toppings')).filter(toppings__in=all_toppings[0], num_toppings__exact=3).filter(toppings__in=all_toppings[1], num_toppings__exact=3).get(toppings__in=all_toppings[2], num_toppings__exact=3)
			else:
				ordered_pizza=Cart_Item.objects.get(pizza=p, cart=cart)
			print(ordered_pizza)
			ordered_pizza.quantity+=int(quantity)
			ordered_pizza.save()
		except Cart_Item.DoesNotExist:
			item=Cart_Item(pizza=p, quantity=quantity, cart=cart)
			item.save()
			for t in all_toppings:
				item.toppings.add(t)
				item.save()
	return render(request, "orders/pizzas.html", context)

# view which manages subs section
def subs(request):
	u=request.user
	cart,created=Cart.objects.get_or_create(cust_id=u.customer)
	context={
		"subs": Sub.objects.all()
	}
	if(request.POST):
		sub_id=request.POST["sub_id"]
		s=Sub.objects.get(id=sub_id)
		quantity=request.POST["quantity"]
		# cart.count+=int(quantity)
		# cart.total+=int(quantity)*s.price
		# cart.save()
		try:
			ordered_sub=Cart_Item.objects.get(sub=s, cart=cart)
			ordered_sub.quantity+=int(quantity)
			ordered_sub.save()
		except Cart_Item.DoesNotExist:
			item=Cart_Item(sub=s, quantity=quantity, cart=cart)
			item.save()
		
	return render(request, "orders/subs.html", context)

# view which handles cart operations
def cart(request):
	u=request.user
	cart,created=Cart.objects.get_or_create(cust_id=u.customer)
	if(created==True):
		context={
		"pizzas": None,
		"subs": None,
		"cart": cart,
		"range": range(1,6)
		}
		return render(request, "orders/cart.html", context)
	else:
		pizzas=Cart_Item.objects.filter(cart=cart).filter(sub__isnull=True)
		subs=Cart_Item.objects.filter(cart=cart).filter(sub__isnull=False)
		context={
		"pizzas": pizzas,
		"subs": subs,
		"cart": cart,
		"range": range(1,6)
		}
		return render(request, "orders/cart.html", context)

# view which handles operations on orders
def order(request):
	if(request.method=="POST"):
		u=request.user
		cart=Cart.objects.get(cust_id=u.customer)
		cart_items=Cart_Item.objects.filter(cart=cart)
		user_order=Order(cust_id=u.customer)
		user_order.save()
		for item in cart_items:
			ordered_item=Order_Item(pizza=item.pizza, sub=item.sub, quantity=item.quantity, order=user_order)
			ordered_item.save()
			if(item.toppings.all()):
				for t in item.toppings.all():
					ordered_item.toppings.add(t)
			ordered_item.save()
			item.delete()
		return render(request, "orders/order_confirm.html", {"order_id": user_order.id})
	else:
		u=request.user
		all_orders=Order.objects.filter(cust_id=u.customer)
		context={"order_items": {}}
		for o in all_orders:
			context["order_items"][o]=o.o_items.all()
		return render(request, "orders/order.html", context)

# view to update quantity in the carts page
@csrf_exempt
def quantity_update(request):
	if(request.method=="POST"):
		item=Cart_Item.objects.get(id=request.POST["cart_item_id"])
		item.quantity=request.POST["new_quantity"]
		item.save()
		return HttpResponseRedirect(reverse('cart'))

# view to remove item in the carts page
@csrf_exempt
def delete_item(request):
	if(request.method=="POST"):
		item=Cart_Item.objects.get(id=request.POST["cart_item_id"]).delete()
		return HttpResponseRedirect(reverse('cart'))
