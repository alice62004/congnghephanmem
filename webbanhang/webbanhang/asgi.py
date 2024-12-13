"""
ASGI config for webbanhang project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

# Nhập module `os` của Python, giúp tương tác với hệ điều hành
import os

# Nhập hàm `get_asgi_application` từ Django, giúp tạo ứng dụng ASGI
from django.core.asgi import get_asgi_application

# Thiết lập biến môi trường `DJANGO_SETTINGS_MODULE`, chỉ định file cấu hình Django
# Ở đây, file cấu hình là `webbanhang.settings`
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webbanhang.settings')

# Tạo một ứng dụng ASGI cho dự án Django
# Biến `application` sẽ là entry point khi triển khai với máy chủ ASGI (như Uvicorn, Daphne)
application = get_asgi_application()

