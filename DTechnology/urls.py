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
from django.urls import path, include
from DTechnology.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path("cart/", cart, name='cart'),
    path('cart/reduce/<int:id>/', reduce_product_quantity, name='reduce_quantity'),
    path('cart/increase/<int:id>/', increase_product_quantity, name='increase_quantity'),
    path('cart/delete/<int:id>/', delete_product, name='delete_product' ),
    path('catalogue/', home, name='home'),
    path('order/', order, name='order'),    
    path('payments/', include('Payments.urls'), name='stripe'),
    path('tracking/', tracking, name="tracking"),
    path('details/<int:id>/', detail, name='details'),
    path('policy/return', return_policy, name='return_policy'),
    path('contact', contact, name = 'contact'),
    path('terms', terms, name = 'terms'),
    path('privacy', privacy, name = 'privacy'),
]
