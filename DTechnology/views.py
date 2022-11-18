from django.shortcuts import render
from django.views.generic import ListView

# view for testing components
def index(request):
    return render(request, 'base_INDEX.html')

def home(request):
    
    return render(request, 'home.html')

class ProductListView(ListView):
    model=Product
    template_name='product_list.html'
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



    def get_queryset(self):

        #Aquí se puede filtrar
        return Product.objects.all()


    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_list'] = Product.objects.all()
        context['titulo'] = 'este es el titulo'
        context['listOfList'] = self.listOfList
        return context
