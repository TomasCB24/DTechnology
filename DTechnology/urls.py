"""DTechnology URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from DTechnology.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path("cart/", cart, name='cart'),
    path('cart/reduce/<int:id>/', reduce_product_quantity, name='reduce_quantity'),
    path('cart/increase/<int:id>/', increase_product_quantity, name='increase_quantity'),
    path('cart/delete/<int:id>/', delete_product, name='delete_product' ),
    path('', home, name='home'),
    path('order/', order, name='order'),
]
