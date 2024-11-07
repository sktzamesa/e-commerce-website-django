from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:product_id>/', views.cart_add, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('orders/', views.order_history, name='order_history'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('', views.cart_view, name='cart_view'),
    path('update/<int:product_id>/', views.update_cart, name='cart_update'),  # Corrected here
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('place_order/', views.place_order, name='place_order'),
    path('update/<int:product_id>/', views.cart_update, name='cart_update'),
    path('home/', views.home_view, name='home_view'),
]
