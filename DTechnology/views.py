from django.shortcuts import render, redirect
from Marketplace.models import *

# view for testing components
def index(request):
    return render(request, 'base_INDEX.html')


def cart(request):

    products = OrderProduct.objects.all()
    # get the total price of the order
    total_price = 0
    total_discount = 0
    for product in products:
        total_price += product.get_final_price()
        total_discount += product.get_amount_saved()

    return render(request, 'base_CART.html', {'products': products, 'total_price': total_price, 'total_discount': total_discount})

def reduce_product_quantity(request, id):
    product = OrderProduct.objects.get(id=id)
    if(product.quantity > 1):
        product.quantity -= 1
        product.save()
    else:
        product.delete()

    return redirect('cart')

def increase_product_quantity(request, id):
    product = OrderProduct.objects.get(id=id)
    product.quantity += 1
    product.save()
    return redirect('cart')


def delete_product(request, id):
    product = OrderProduct.objects.get(id=id)
    product.delete()
    return redirect('cart')