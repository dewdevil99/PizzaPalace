from django.urls import path

from . import views

urlpatterns = [
	path("", views.index, name="index"),
	path("register", views.register, name="register"),
    path("profile", views.profile, name="profile"),
    path("logout", views.logout_view, name="logout"),
    path("pizzas", views.pizzas, name="pizzas"),
    path("subs", views.subs, name="subs"),
    path("cart", views.cart, name="cart"),
    path("order", views.order, name="order"),
    path("quantity_update", views.quantity_update, name="quantity_update"),
    path("delete_item", views.delete_item, name="delete_item")
]
