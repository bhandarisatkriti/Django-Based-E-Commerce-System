"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
<<<<<<< HEAD
from django.urls import path, include
=======
from django.urls import path,include
>>>>>>> cc0a37d0ea15a7c8f692c929f1e1b6f3d991b04c

from django.conf.urls.static import static

from . import settings
urlpatterns = [
<<<<<<< HEAD
    path('admin/', admin.site.urls),    
    path('', include('store.urls')),  # Include store app URLs
    path('users/', include('users.urls')),  # Include user app URLs
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    
=======
    path('admin/', admin.site.urls),
    path('',include('users.urls'))
]
>>>>>>> cc0a37d0ea15a7c8f692c929f1e1b6f3d991b04c
