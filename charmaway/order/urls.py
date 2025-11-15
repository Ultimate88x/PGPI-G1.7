from django.urls import path
from . import views

urlpatterns = [
    path("cart/", views.view_cart, name="view_cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/decrease/<int:product_id>/", views.decrease_from_cart, name="decrease_from_cart"),
    path("cart/remove/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/clear/", views.clear_cart, name="clear_cart"),
    path("cart/checkout/", views.checkout, name="checkout"),
    path("success/<int:order_id>/", views.order_success, name="order_success"),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('lookup/', views.order_lookup, name='order_lookup'),
]
