from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='checkout'),
    path('config/', views.stripe_config, name='config'),  
    path('create-checkout-session/', views.create_checkout_session), 
    path('success/', views.SuccessView, name='success'), 
    path('cancelled/', views.CancelledView, name='cancelled'),
]