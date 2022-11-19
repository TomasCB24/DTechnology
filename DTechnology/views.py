from django.shortcuts import render
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt

from Marketplace.models import Product, CATEGORY_CHOICES, DEPARTMENT_CHOICES, PRODUCER_CHOICES

# view for testing components
def index(request):
    return render(request, 'base_INDEX.html')

@csrf_exempt
def home(request):

    active_category, active_department, active_producer = 'Any Categories', 'Any Departments', 'Any Producers'

    if request.method == 'POST':
        category = request.POST.get('Categories')
        department = request.POST.get('Departments')
        producer = request.POST.get('Producers')
        active_category, active_department, active_producer = category, department, producer
    
    products = get_products(active_category, active_department, active_producer)

    return render(request, 'home.html', 
            {'categories': CATEGORY_CHOICES, 
            'departments': DEPARTMENT_CHOICES, 
            'producers': PRODUCER_CHOICES, 
            'active_cat': active_category, 
            'active_dep': active_department, 
            'active_prod': active_producer,
            'listOfList': products}
        )

def get_products(category, department, producer):
    
    listOfList = []

    if category == 'Any Categories':
        category = ''
    if department == 'Any Departments':
        department = ''
    if producer == 'Any Producers':
        producer = ''
    
    productos = Product.objects.filter(section__icontains=category, department__icontains=department, producer__icontains=producer)

    i=0
    listaCuatroProductos = []
    for producto in productos:
        if i == 4:
            listOfList.append(listaCuatroProductos)
            listaCuatroProductos = []
            i=0
        listaCuatroProductos.append(producto)
        i+=1
    if len(listaCuatroProductos) < 4:
        listOfList.append(listaCuatroProductos)    
    return listOfList

