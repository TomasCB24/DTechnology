from datetime import datetime
from django.shortcuts import render, redirect
from Marketplace.models import *
from django.shortcuts import render
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib import messages
from .forms import AddressForm
from django.http import HttpResponseRedirect
from django_countries import countries

from Marketplace.models import Product, CATEGORY_CHOICES, DEPARTMENT_CHOICES, PRODUCER_CHOICES

def get_cart_counter(request):
    if 'nonuser' in request.session:
        order_products = OrderProduct.objects.filter(session_id=request.session['nonuser'])
        cart_counter = 0
        for order_product in order_products:
            cart_counter += order_product.quantity
        return cart_counter
    else:
        return 0

def cart(request):

    product_orders = OrderProduct.objects.filter(session_id=request.session['nonuser'])
    # get the total price of the order
    total_price = 0
    for product_order in product_orders:
        total_price += product_order.get_final_price()

    return render(request, 'base_CART.html', {'products': product_orders, 'total_price': total_price, 'cart_counter': get_cart_counter(request)})

def reduce_product_quantity(request, id):
    product = OrderProduct.objects.get(id=id)
    if(product.quantity > 1):
        product.quantity -= 1
        product.save()
    else:
        product.delete()

    return redirect('cart')

def increase_product_quantity(request, id):
    orderProduct = OrderProduct.objects.get(id=id)
    product = orderProduct.product
    
    order_products = OrderProduct.objects.filter(product=product)
    cart_quantity = 0
    for order_product in order_products:
        cart_quantity += order_product.quantity
    
    if 0 < (product.inventory - cart_quantity):
        orderProduct.quantity += 1
        orderProduct.save()
    else:
        messages.warning(request, 'No hay suficientes ' + product.title + ' en el inventario')
    return redirect('cart')


def delete_product(request, id):
    product = OrderProduct.objects.get(id=id)
    product.delete()
    return redirect('cart')

@csrf_exempt
def home(request):

    if 'nonuser' not in request.session or request.session['nonuser'] == '':
        request.session['nonuser'] = str(uuid.uuid4())
    
    active_category, active_department, active_producer = 'Any Categories', 'Any Departments', 'Any Producers'
    search = ""

    if request.method == 'POST':
        search = request.POST.get("search-product", '')
        if 'filter' in request.POST:
            category = request.POST.get('Categories', 'Any Categories')
            department = request.POST.get('Departments', 'Any Departments')
            producer = request.POST.get('Producers', 'Any Producers')
            active_category, active_department, active_producer = category, department, producer
            
        elif 'add_to_cart' in request.POST:
            quantity = int(request.POST.get('quantity'))
            product_id = request.POST.get('product_id')

            product = Product.objects.get(id=product_id)

            order_products = OrderProduct.objects.filter(product=product)

            cart_quantity = 0
            for order_product in order_products:
                cart_quantity += order_product.quantity
            
            if((product.inventory - cart_quantity) >= quantity):
                add_to_cart(request,product_id, quantity)
            else:
                messages.warning(request, 'No hay suficientes ' + product.title + ' en el inventario')
            
    products = get_products(active_category, active_department, active_producer, search)

    return render(request, 'base_HOME.html', 
            {'categories': CATEGORY_CHOICES, 
            'departments': DEPARTMENT_CHOICES, 
            'producers': PRODUCER_CHOICES, 
            'active_cat': active_category, 
            'active_dep': active_department, 
            'active_prod': active_producer,
            'listOfList': products,
            'cart_counter': get_cart_counter(request)
            }
        )

def add_to_cart(request,product_id, quantity):

    try:
        product = Product.objects.get(id=product_id)
        order_product = OrderProduct.objects.get(product=product, session_id=request.session['nonuser'])

        order_product.add_products(quantity)
    except:
        OrderProduct.objects.create(product=product, quantity=quantity, session_id = request.session['nonuser'])

def get_products(category, department, producer, search):
    
    listOfList = []

    if category == 'Any Categories':
        category = ''
    if department == 'Any Departments':
        department = ''
    if producer == 'Any Producers':
        producer = ''
    
    productos = Product.objects.filter(section__icontains=category, 
                                        department__icontains=department, 
                                        producer__icontains=producer).filter(Q(title__icontains=search) |
                                                                            Q(section__icontains=search) | 
                                                                            Q(department__icontains=search) | 
                                                                            Q(producer__icontains=search))   

    i=0
    listaCuatroProductos = []
    for producto in productos:
        if i == 4:
            listOfList.append(listaCuatroProductos)
            listaCuatroProductos = []
            i=0
        listaCuatroProductos.append(producto)
        i+=1
    if len(listaCuatroProductos) <= 4:
        listOfList.append(listaCuatroProductos)  
    
    return listOfList


def order(request):
    
    product_orders = OrderProduct.objects.filter(session_id=request.session['nonuser'])
    # get the total price of the order
    total_price = 0
    for product_order in product_orders:
        total_price += product_order.get_final_price()
   
    if request.method == 'POST':
        form = AddressForm(request.POST)
                
        if form.is_valid():
            email = request.POST.get("email")
            address = request.POST.get("street_address")
            if Address.objects.filter(email = email,street_address = address).count() == 0:
                Address.objects.create(**form.cleaned_data)
            
            product_orders = OrderProduct.objects.filter(session_id=request.session['nonuser'])

            shipping = Address.objects.get(email = email,street_address = address)
            order = Order.objects.create(shipping_address = shipping, billing_address = shipping)
            order.products.set(product_orders)
            order.save()

            request.session['order_id'] = order.ref_id

            payment = request.POST.get("payment")
            if payment == 'Contrareembolso':
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
            print(Order.objects.all())
            order = [x for x in Order.objects.all() if x.ref_code == order_code][0]
            print("Pedido",order)
            print(order.ordered_date)
            ordered2 = order.ordered
            print(ordered2)
            being_delivered2 = order.being_delivered
            print(being_delivered2)
            delivered2 = order.received
            print(delivered2)

            print(ordered2, being_delivered2, delivered2)

            is_delivered = False
            is_being_delivered = False
            is_ordered = False
            
            if delivered2:
                is_delivered = True
            elif being_delivered2:
                is_being_delivered = True
            elif ordered2:
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
    return render(request, 'base_TRACKING.html')
