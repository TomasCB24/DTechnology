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
from django.core.paginator import Paginator

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

def index(request):
    return render(request, 'base_INDEX.html', {'cart_counter': get_cart_counter(request)})

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
    
    if request.GET.get('search'):
        search = request.GET.get('search')
    if request.GET.get('category'):
        active_category = request.GET.get('category')
    if request.GET.get('department'):
        active_department = request.GET.get('department')
    if request.GET.get('producer'):
        active_producer = request.GET.get('producer')
    [products, page_obj] = get_products(active_category, active_department, active_producer, search, request, page_size=12)
    print(products)

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

def add_to_cart(request,product_id, quantity):

    try:
        product = Product.objects.get(id=product_id)
        order_product = OrderProduct.objects.get(product=product, session_id=request.session['nonuser'])

        order_product.add_products(quantity)
    except:
        OrderProduct.objects.create(product=product, quantity=quantity, session_id = request.session['nonuser'])

def get_products(category, department, producer, search, request, page_size):
    
    listOfList = []

    if category == 'Cualquier Categoría':
        category = ''
    if department == 'Cualquier Departamento':
        department = ''
    if producer == 'Cualquier Fabricante':
        producer = ''
    
    productos = Product.objects.filter(section__icontains=category, 
                                        department__icontains=department, 
                                        producer__icontains=producer).filter(Q(title__icontains=search) |
                                                                            Q(section__icontains=search) | 
                                                                            Q(department__icontains=search) | 
                                                                            Q(producer__icontains=search))   

    paginator = Paginator(productos, page_size) # Show 5 products per page.
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)
    i=0
    listaCuatroProductos = []
    for producto in products_page:
        if i == 4:
            listOfList.append(listaCuatroProductos)
            listaCuatroProductos = []
            i=0
        listaCuatroProductos.append(producto)
        i+=1
    if len(listaCuatroProductos) <= 4 and len(productos)!=0:
        listOfList.append(listaCuatroProductos)  
    
    return [listOfList, products_page]


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
        
        quan= int(request.POST.get('quantity'))
        pro_id = request.POST.get('product_id')

        pro = Product.objects.get(id=pro_id)

        order_products = OrderProduct.objects.filter(product=pro)

        cart_quan = 0
        for ord_pro in order_products:
            cart_quan += ord_pro.quantity
        
        if((pro.inventory - cart_quan) >= quan):
            add_to_cart(request,pro_id, quan)
        else:
            messages.warning(request, 'No hay suficientes ' + pro.title + ' en el inventario')
    
    return render(request, 'base_DETAILS.html', 
                            {'product': pro,
                            'cart_counter': get_cart_counter(request)
                            })

def return_policy(request):
    return render(request, 'base_RETURN_POLICY.html')

def contact(request):
    return render(request, 'base_CONTACT.html', {'cart_counter': get_cart_counter(request)})

