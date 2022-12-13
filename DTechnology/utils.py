from Marketplace.models import *
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.contrib import messages

def get_cart_counter(request):
    if 'nonuser' in request.session:
        order_products = OrderProduct.objects.filter(session_id=request.session['nonuser']).filter(ordered=False)
        cart_counter = 0
        for order_product in order_products:
            cart_counter += order_product.quantity
        return cart_counter
    else:
        return 0


def add_product_to_cart(request):
    quantity = int(request.POST.get('quantity'))
    product_id = request.POST.get('product_id')

    product = Product.objects.get(id=product_id)
    
    order_product = OrderProduct.objects.filter(product=product).filter(ordered=False, session_id=request.session['nonuser'])

    if not order_product.exists():
        if quantity <= product.get_stock():
            order_product = OrderProduct.objects.create(product=product, quantity=quantity, session_id=request.session['nonuser'])
            order_product.save()
        else:
            messages.warning(request, 'No hay suficientes ' + product.title + ' en el inventario')

    else:
        order_product = order_product[0]

        if 0 <= (product.get_stock() - quantity):
            order_product.quantity += quantity
            order_product.save()
        else:
            messages.warning(request, 'No hay suficientes ' + product.title + ' en el inventario')


def delete_product(request, id):
    product = OrderProduct.objects.get(id=id)
    product.delete()
    return redirect('cart')


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
    
    order_products = OrderProduct.objects.filter(product=product).filter(ordered = False)
    cart_quantity = 0
    for order_product in order_products:
        cart_quantity += order_product.quantity
    
    if 0 < (product.inventory - cart_quantity):
        orderProduct.quantity += 1
        orderProduct.save()
    else:
        messages.warning(request, 'No hay suficientes ' + product.title + ' en el inventario')
    return redirect('cart')


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
