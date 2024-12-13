from django.contrib import admin
from .models import *

# Đăng ký các model vào trang quản trị Django.
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(BlogPost)

