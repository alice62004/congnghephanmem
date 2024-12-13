from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from .models import Category, Customer, Order, OrderItem, Product   
import json
from django.contrib.auth.decorators import login_required
# Tạo Customer khi User được tạo
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.views.decorators.csrf import csrf_exempt
from .models import Invoice
from datetime import datetime
from .models import ShippingAddress
from django.contrib import admin
from django.views.decorators.csrf import csrf_protect




@receiver(post_save, sender=User)
def create_customer_for_user(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)

# Trang chủ
def home(request):
    categories = Category.objects.filter(is_sub=False)  # Lấy danh mục cha
    items, cartItems, order = [], 0, {'get_cart_items': 0, 'get_cart_total': 0}

    if request.user.is_authenticated:
        try:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.items.all()
            cartItems = order.get_cart_items
        except ObjectDoesNotExist:
            pass  # Không làm gì nếu không tìm thấy Customer

    products = Product.objects.all()  # Lấy tất cả sản phẩm
    context = {'products': products, 'cartItems': cartItems, 'categories': categories}
    return render(request, 'app/home.html', context)
def login_view(request):
    if request.method == "POST":
        # Assuming the login logic is here
        # If login is successful
        messages.success(request, "You have logged in successfully!")
        return redirect('home')
def logout_view(request):
    logout(request)
    return redirect('login')
# Chi tiết sản phẩm
def detail(request):
    items, cartItems, order = [], 0, {'get_cart_items': 0, 'get_cart_total': 0}
    
    if request.user.is_authenticated:
        try:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.items.all()
            cartItems = order.get_cart_items
        except ObjectDoesNotExist:
            pass

    id = request.GET.get('id', '')
    products = Product.objects.filter(id=id)
    context = {'products': products, 'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'app/detail.html', context)

# Hiển thị danh mục sản phẩm
def category(request):
    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get('category', '')
    products = Product.objects.filter(Category__slug=active_category) if active_category else []
    context = {'categories': categories, 'products': products, 'active_category': active_category}
    return render(request, 'app/category.html', context)
def category_view(request):
    category_slug = request.GET.get('category')
    if category_slug:
        try:
            category = Category.objects.get(slug=category_slug)
            products = Product.objects.filter(category=category)
        except Category.DoesNotExist:
            category = None
            products = []
    else:
        products = Product.objects.all()

    context = {
        'categories': Category.objects.all(),  # Hiển thị danh sách danh mục
        'products': products,                  # Sản phẩm trong danh mục đã chọn
    }
    return render(request, 'category.html', context)
# Tìm kiếm sản phẩm
def search(request):
    keys, searched = [], ""
    if request.method == "POST":
        searched = request.POST.get("searched", "")
        keys = Product.objects.filter(name__icontains=searched)
    return render(request, 'app/search.html', {"searched": searched, "keys": keys})

# Đăng ký người dùng
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('password1')
            
            if User.objects.filter(username=username).exists():
                form.add_error('username', "Tên người dùng đã tồn tại")
                return render(request, 'app/register.html', {'form': form})
            
            form.save()
            messages.success(request, "Đăng ký thành công!")
            return redirect('login')
        else:
    
            return render(request, 'app/register.html', {'form': form})
    else:
        form = UserCreationForm()
    return render(request, 'app/register.html', {'form': form})



def home(request):
    categorys = Category.objects.all() 
    products = Product.objects.all()

  
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)  

    return render(request, 'app/home.html', {'products': products, 'categorys': categorys})

def loginPage(request):
    form = AuthenticationForm()
    error_message = None
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                error_message("", 'Tên đăng nhập hoặc mật khẩu không đúng')  
    context = { 'form': form,
        'error_message': error_message}
    return render(request, 'app/login.html', {'error_message': error_message})
def logoutPage(request):
    logout(request)
    return redirect('login')
# Giỏ hàng
def cart(request):
    items, cartItems, order = [], 0, {'get_cart_items': 0, 'get_cart_total': 0}

    if request.user.is_authenticated:
        try:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.items.all()
            cartItems = order.get_cart_items

         
            for item in items:
                item.product.price_formatted = "{:,.0f}".format(item.product.price).replace(",", ".") + " đ"
                item.total_formatted = "{:,.0f}".format(item.get_total).replace(",", ".") + " đ"

        
            order.cart_total_formatted = "{:,.0f}".format(order.get_cart_total).replace(",", ".") + " đ"
        except ObjectDoesNotExist:
            pass

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }
    return render(request, 'app/cart.html', context)


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order, created = Order.objects.get_or_create(user=request.user, complete=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    order_item.quantity += 1
    order_item.save()
    return redirect('cart')
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    

    order = Order.objects.get(customer=request.user.customer, complete=False)
    
    order_item = OrderItem.objects.filter(order=order, product=product).first()
    
    if order_item:
        order_item.delete()
        
    return redirect('cart')

@csrf_exempt
def update_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if request.user.is_authenticated:
            customer = request.user.customer
            order = Order.objects.get(customer=customer, complete=False)
            item = order.items.get(product_id=product_id)
            item.quantity = quantity
            item.save()
    return redirect('cart')

# Thanh toán
def checkout(request):
    items, cartItems, order = [], 0, {'get_cart_items': 0, 'get_cart_total': 0}

    if request.user.is_authenticated:
        try:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.items.all()
            cartItems = order.get_cart_items
        except ObjectDoesNotExist:
            pass

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'app/checkout.html', context)




def checkout_payment(request):
    # Xử lý thanh toán
    if request.method == 'POST':
        # Lấy thông tin từ form
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        total_amount = request.POST.get('total_amount')
        payment_status = 'Đang xử lý'  # Giả sử thanh toán đang được xử lý
        payment_date = datetime.now().strftime('%d-%m-%Y %H:%M:%S')  # Lấy ngày giờ thanh toán hiện tại
        order_id = 'DH001'  # Mã đơn hàng

        # Lưu thông tin vào session hoặc cơ sở dữ liệu
        request.session['invoice_data'] = {
            'order_id': order_id,
            'name': name,
            'email': email,
            'address': address,
            'city': city,
            'total_amount': total_amount,
            'payment_status': payment_status,
            'payment_date': payment_date,
        }

        # Redirect tới trang lịch sử (lichsu)
        return redirect('lichsu')

def product_detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'product_detail.html', {'product': product})
# Cập nhật sản phẩm trong giỏ hàng
@csrf_exempt
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    try:
        customer = request.user.customer
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Customer does not exist'}, status=400)

    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was updated', safe=False)
def intro(request):
    return render(request, 'app/intro.html')

@csrf_exempt
def save_invoice(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        invoice = Invoice.objects.create(
            name=data['name'],
            email=data['email'],
            address=data['address'],
            city=data['city'],
            total_amount=data['total_amount'],
        )
        return JsonResponse({'message': 'Invoice saved successfully!', 'invoice_id': invoice.id})
def lichsu(request):
    order_id = request.session.get('order_id', 'Không có mã đơn hàng')
    total_amount = request.session.get('total_amount', 0.0)  # Giá trị mặc định
    payment_date = request.session.get('payment_date', 'Chưa cập nhật')
    return render(request, 'app/lichsu.html', {
        'order_id': order_id,
        'total_amount': total_amount,
        'payment_date': payment_date
    })

class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'city', 'state', 'zipcode', 'country')
    search_fields = ('user__username', 'address', 'city', 'state', 'zipcode', 'country')

