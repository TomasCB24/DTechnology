from django.shortcuts import render
from django.views.generic import ListView

from Marketplace.models import Product

# view for testing components
def index(request):
    return render(request, 'base_INDEX.html')


class ProductListView(ListView):
    model=Product
    template_name='home.html'
    listOfList = []
    productos = Product.objects.all()
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


    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['listOfList'] = self.listOfList
        return context
