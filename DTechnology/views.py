from django.shortcuts import render
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from Marketplace.models import Product, CATEGORY_CHOICES, DEPARTMENT_CHOICES, PRODUCER_CHOICES

# view for testing components
def index(request):
    return render(request, 'base_INDEX.html')

@csrf_exempt
def home(request):

    active_category, active_department, active_producer = 'Any Categories', 'Any Departments', 'Any Producers'
    search = ""

    if request.method == 'POST':
        search = request.POST.get("search-product", '')
        category = request.POST.get('Categories', 'Any Categories')
        department = request.POST.get('Departments', 'Any Departments')
        producer = request.POST.get('Producers', 'Any Producers')
        active_category, active_department, active_producer = category, department, producer
    
    products = get_products(active_category, active_department, active_producer, search)

    return render(request, 'base_HOME.html', 
            {'categories': CATEGORY_CHOICES, 
            'departments': DEPARTMENT_CHOICES, 
            'producers': PRODUCER_CHOICES, 
            'active_cat': active_category, 
            'active_dep': active_department, 
            'active_prod': active_producer,
            'listOfList': products}
        )

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
        print(producto.section)
        if i == 4:
            listOfList.append(listaCuatroProductos)
            listaCuatroProductos = []
            i=0
        listaCuatroProductos.append(producto)
        i+=1
    if len(listaCuatroProductos) < 4:
        listOfList.append(listaCuatroProductos)    
    return listOfList

