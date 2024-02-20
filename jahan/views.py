from django.shortcuts import render
from  store.models import Product, ReviewRating
from category.models import Category

def home(request):
    products = Product.objects.all().filter(is_available=True).order_by('-created_date')
    reviews = []  # Define an empty list as the default value for reviews

    for product in products:
        reviews += ReviewRating.objects.filter(product_id=product.id, status=True)

    context = {
        'products': products,
        'reviews': reviews,
    }
    return render(request, 'home.html', context)

def sidebar_categories(request):
    categories = Category.objects.all()  
    return render(request, 'sidebar.html', {'categories': categories})