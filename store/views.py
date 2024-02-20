from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from .models import Product, ReviewRating, ProductGallery, Category
from category.models import Category
from carts.views import _cart_id, CartItem
# Create your views here.
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from .forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct
from random import sample

def collections(request):
    category = Category.objects.filter(status=0)
    context = {
        'category' : category,
    }
    return render(request, "store/collections.html", context)

def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 9)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count= products.count()

    else:
        products = Product.objects.all().filter(is_available=True).order_by('-created_date')
        paginator = Paginator(products, 9)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        'products': paged_products,
        'product_count' : product_count,
    }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
        

    except Exception as e:
        raise e
    if request.user.is_authenticated:
        try:
            orderproduct =OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)
    variations = single_product.variation_set.all()
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)
    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'orderproduct' : orderproduct,
        'reviews' : reviews,
        'product_gallery' : product_gallery,
        'variations' : variations,
    }
    return render(request, 'store/product_detail.html', context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count= products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)

def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, "متشکریم، نظر شما به روز رسانی شد")
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating  = form. cleaned_data['rating']
                data.review  = form. cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, "ممنون! نظر شما با موفقیت ثبت شد.")
                return redirect(url)

def random_slider(request):
    categories = Category.objects.all()
    random_categories = sample(list(categories), min(len(categories), 5))  # Select up to 5 random categories
    context = {
        'random_categories': random_categories,
        'category_names': [category.category_name for category in random_categories]
        }
    return render(request, 'include/random_slider.html', context)

def navbar(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'navbar.html', {'products': products, 'categories': categories})