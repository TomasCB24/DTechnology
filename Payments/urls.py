from django.urls import path

from . import views

urlpatterns = [
    path('config/', views.stripe_config, name='config'),  
    path('create-checkout-session/', views.create_checkout_session), 
    path('success/', views.success_view, name='success'), 
    path('cancelled/', views.cancelled_view, name='cancelled'),
]