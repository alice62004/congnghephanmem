"""
WSGI config for webbanhang project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""
import os

from django.core.wsgi import get_wsgi_application

# Thiết lập biến môi trường 'DJANGO_SETTINGS_MODULE' cho dự án Django.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webbanhang.settings')

# Lấy đối tượng WSGI cho ứng dụng Django, giúp tương tác với web server.
application = get_wsgi_application()

