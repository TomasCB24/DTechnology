from django.shortcuts import render

# view for testing components
def index(request):
    return render(request, 'base_INDEX.html')