from datetime import datetime
from django.shortcuts import render

from django.conf import settings 
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.views.generic.base import TemplateView
import stripe

from Marketplace.models import Order, OrderProduct

from static.python.utils import send_email

@csrf_protect
@require_http_methods(["GET"])
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

@csrf_protect
@require_http_methods(["GET"])
def create_checkout_session(request):
  if request.method == 'GET':
    domain_url = 'http://localhost:8000/payments/'
    stripe.api_key = settings.STRIPE_SECRET_KEY
    
    try:
      product_orders = OrderProduct.objects.filter(session_id=request.session['nonuser']).filter(ordered=False)
      
      line_items = []
      for product_order in product_orders:
        price = product_order.get_final_price() / product_order.quantity
        line_items.append({
          'price_data': {
            'currency': 'eur',
            'product_data': {
              'name': product_order.product.title,
              'images': [product_order.product.image],
            },
            'unit_amount': int(price * 100),
          },
          'quantity': product_order.quantity,
        })
      
      checkout_session = stripe.checkout.Session.create(
        success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=domain_url + 'cancelled/',
        payment_method_types=['card'],
        mode='payment',
        line_items=line_items,
      )
                
      return JsonResponse({'sessionId': checkout_session['id']})
    except Exception as e:
      return JsonResponse({'error': str(e)})

@require_http_methods(["GET"])
def success_view(request):

    template_name = 'payments/success.html'
    order_id = request.session['order_id']
    order = Order.objects.get(ref_id=int(order_id))

    order.ordered = True
    order.ordered_date = datetime.now()
    order.save()
    product_orders = OrderProduct.objects.filter(session_id=request.session['nonuser']).filter(ordered=False)
    
    #Send email to customer
    send_email(order, product_orders)
    
    for product_order in product_orders:
      product_order.ordered = True
      product_order.save()
      quantity = product_order.quantity
      product = product_order.product
      product.inventory -= quantity
      product.save()

    #delete the order id from the session
    del request.session['order_id']

    return render(request , template_name)

@require_http_methods(["GET"])
def cancelled_view(request):
    template_name = 'payments/cancelled.html'
    order_id = request.session['order_id']
    order = Order.objects.get(ref_id=int(order_id))
    order.delete()
    
    return render(request , template_name)

