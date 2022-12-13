from django.shortcuts import render, redirect
from Marketplace.models import *
from django.shortcuts import render
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .forms import AddressForm
from django.http import HttpResponseRedirect
from django_countries import countries
from DTechnology.utils import *

from Marketplace.models import Product, CATEGORY_CHOICES, DEPARTMENT_CHOICES, PRODUCER_CHOICES

def index(request):
    return render(request, 'base_INDEX.html', {'cart_counter': get_cart_counter(request)})

def cart(request):
    product_orders = OrderProduct.objects.filter(session_id=request.session['nonuser']).filter(ordered=False)
    # get the total price of the order
    total_price = 0
    for product_order in product_orders:
        total_price += product_order.get_final_price()

    return render(request, 'base_CART.html', {'products': product_orders, 'total_price': total_price, 'cart_counter': get_cart_counter(request)})

def home(request):

    if 'nonuser' not in request.session or request.session['nonuser'] == '':
        request.session['nonuser'] = str(uuid.uuid4())
    
    active_category, active_department, active_producer = 'Cualquier Categoría', 'Cualquier Departamento', 'Cualquier Fabricante'
    search = ""

    if request.method == 'POST':
        search = request.POST.get("search-product", '')
        if 'filter' in request.POST:
            category = request.POST.get('Categoría', 'Cualquier Categoría')
            department = request.POST.get('Departamento', 'Cualquier Departamento')
            producer = request.POST.get('Fabricante', 'Cualquier Fabricante')
            active_category, active_department, active_producer = category, department, producer
            
        elif 'add_to_cart' in request.POST:
            add_product_to_cart(request)
        
    if request.GET.get('search'):
        search = request.GET.get('search')
    if request.GET.get('category'):
        active_category = request.GET.get('category')
    if request.GET.get('department'):
        active_department = request.GET.get('department')
    if request.GET.get('producer'):
        active_producer = request.GET.get('producer')
    [products, page_obj] = get_products(active_category, active_department, active_producer, search, request, page_size=12)

    return render(request, 'base_CATALOGUE.html', 
            {'categories': CATEGORY_CHOICES, 
            'departments': DEPARTMENT_CHOICES, 
            'producers': PRODUCER_CHOICES, 
            'active_cat': active_category, 
            'active_dep': active_department, 
            'active_prod': active_producer,
            'listOfList': products,
            'cart_counter': get_cart_counter(request),
            'page_obj': page_obj,
            'active_category': active_category,
            'active_department': active_department,
            'active_producer': active_producer,
            'search': search,
            }
        )

def order(request):
    
    product_orders = OrderProduct.objects.filter(session_id=request.session['nonuser']).filter(ordered=False)
    # get the total price of the order
    total_price = 0
    for product_order in product_orders:
        total_price += product_order.get_final_price()
   
    if request.method == 'POST':
        form = AddressForm(request.POST)
                
        if form.is_valid():
            email = request.POST.get("email")
            address = request.POST.get("street_address")
            pay = request.POST.get("payment")
            name = request.POST.get("name")
            surname = request.POST.get("surname")
            phone = request.POST.get("phone")
            
            
            if Address.objects.filter(email = email,street_address = address).count() == 0:
                #create address by form
                adr = Address(**form.cleaned_data)
                adr.save()
            else:
                shipping = Address.objects.get(email = email,street_address = address)
                shipping.payment = pay
                shipping.name = name
                shipping.surname = surname
                shipping.phone = phone
                shipping.save()
                
            product_orders = OrderProduct.objects.filter(session_id=request.session['nonuser']).filter(ordered=False)      
            
            shipping = Address.objects.get(email = email,street_address = address)
            order = Order.objects.create(shipping_address = shipping, billing_address = shipping)
            order.products.set(product_orders)
            order.save()

            request.session['order_id'] = order.ref_id

            payment = request.POST.get("payment")
            if payment == 'Contra reembolso':
                return redirect('success')
            
            return render(request, 'payments/redirect_STRIPE.html', {'order': order})

        
    else:
        

        form = AddressForm()

    return render(request, 'base_ORDER.html', 
                            {'form': form,
                            'total_price': total_price,
                            'cart_counter': get_cart_counter(request)
                            })

def tracking(request):
    if request.method == 'POST':
        order_code = request.POST.get('search-order')

        try:
            order = [x for x in Order.objects.all() if x.ref_code == order_code][0]
            ordered = order.ordered
            being_delivered = order.being_delivered
            delivered = order.received

            is_delivered = False
            is_being_delivered = False
            is_ordered = False
            
            if delivered:
                is_delivered = True
            elif being_delivered:
                is_being_delivered = True
            elif ordered:
                is_ordered = True

            return render(request, 'base_TRACKING.html', 
                            {'is_ordered': is_ordered,
                            'is_being_delivered': is_being_delivered,
                            'is_delivered': is_delivered,
                            'cart_counter': get_cart_counter(request)
                            })
        except:
            messages.warning(request, 'No se ha encontrado el pedido')
            return redirect('tracking')
    return render(request, 'base_TRACKING.html', {'cart_counter': get_cart_counter(request)})

def detail(request,id):
    pro = Product.objects.get(id=id)
    
    if request.method == 'POST' and 'add_to_cart' in request.POST:
        add_product_to_cart(request)
    
    return render(request, 'base_DETAILS.html', 
                            {'product': pro,
                            'cart_counter': get_cart_counter(request)
                            })

def return_policy(request):
    return render(request, 'base_RETURN_POLICY.html')

def contact(request):
    return render(request, 'base_CONTACT.html', {'cart_counter': get_cart_counter(request)})

def terms(request):
    return render(request, 'base_TERMS.html', {'cart_counter': get_cart_counter(request)})

def privacy(request):
    return render(request, 'base_PRIVACY.html', {'cart_counter': get_cart_counter(request)})
