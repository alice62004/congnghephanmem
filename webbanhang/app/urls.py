# app/urls.py
# Import các module cần thiết từ Django
from django.urls import path  # Import hàm path để định nghĩa các URL
from . import views  # Import các hàm view từ file views.py
from django.contrib import admin

# Danh sách URL patterns
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.loginPage, name='login'),
    path('intro', views.intro, name='intro'),
    path('checkout/payment/', views.checkout_payment, name='checkout_payment'),
    path('logout/', views.logoutPage, name='logout'),
    path('search/', views.search, name='search'),
    path('category/', views.category, name='category'),
    path('detail/', views.detail, name='detail'),
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
     path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:product_id>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('detail/<int:id>/', views.product_detail, name='detail'),
    path('lichsu/', views.lichsu, name='lichsu'),
    
 
]
