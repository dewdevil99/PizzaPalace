from django.contrib import admin

# Register your models here.
from .models import Customer, Pizza, Topping, Sub, Cart, Cart_Item, Order, Order_Item

class Cart_ItemInline(admin.TabularInline):
	model=Cart_Item
	extra=0

class CartAdmin(admin.ModelAdmin):
	inlines=[
	Cart_ItemInline,
	]

class Order_ItemInline(admin.TabularInline):
	model=Order_Item
	extra=0

class OrderAdmin(admin.ModelAdmin):
	inlines=[
	Order_ItemInline,
	]

admin.site.register(Customer)
admin.site.register(Order_Item)
admin.site.register(Order, OrderAdmin)
admin.site.register(Pizza)
admin.site.register(Topping)
admin.site.register(Sub)
admin.site.register(Cart_Item)
admin.site.register(Cart, CartAdmin)