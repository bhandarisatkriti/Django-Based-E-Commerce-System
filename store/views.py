from django.shortcuts import render

from store.models import Product

def home(request):
    products = Product.objects.all()

    return render (request, 'store/home.html', {'products': products} )

def about(request):
    return render (request, 'store/about.html')