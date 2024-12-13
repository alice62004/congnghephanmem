# Python biểu diễn cấu trúc của bảng cơ sở dữ liệu
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

from django.db import models

class Category(models.Model):
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='sub_categories', null=True, blank=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200, null=False)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']
        
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=False)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    categories = models.ManyToManyField(Category, related_name='products')  
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    detail = models.TextField(null=True,blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE,default=1)
    def __str__(self):
        return self.name

    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''  # Trả về đường dẫn mặc định nếu không có hình ảnh
        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)
    payment_status = models.CharField(max_length=100, null=True, default="Pending")

    def __str__(self):
        if self.id is not None:
            return f"Order {self.id}"
        else:
            return "Order mới"

    @property
    def get_cart_items(self):
        order_items = self.items.all()
        total_items = sum([item.quantity for item in order_items])
        return total_items

    @property
    def get_cart_total(self):
        order_items = self.items.all()
        total = sum([item.get_total for item in order_items])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True, related_name="items")
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(default=timezone.now)

    @property
    def get_total(self):
        # Kiểm tra nếu sản phẩm có hợp lệ không
        if self.product:
            total = self.product.price * self.quantity  # Tính tổng tiền của sản phẩm
            return total
        return 0  # Trả về 0 nếu không có sản phẩm

    def __str__(self):
        return str(self.product)

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    mobile = models.CharField(max_length=255)
    date_added = models.DateTimeField(default=timezone.now)


class Invoice(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    total_amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice {self.id} - {self.name}"
class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
