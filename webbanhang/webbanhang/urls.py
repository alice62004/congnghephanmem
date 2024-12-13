"""
URL configuration for webbanhang project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),  # Đường dẫn tới trang quản trị của Django
    path('', include('app.urls')),    # Đường dẫn chính của ứng dụng, bao gồm các URL từ 'app.urls'
]

# Cấu hình MEDIA_URL để Django phục vụ các tệp media
MEDIA_URL = '/images/'

# Thêm đường dẫn cho tệp media vào urlpatterns.
# Cấu hình này giúp Django phục vụ các tệp media (như hình ảnh, tài liệu) từ thư mục MEDIA_ROOT khi phát triển.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

