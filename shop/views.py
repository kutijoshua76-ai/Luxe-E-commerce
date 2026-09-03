from django.shortcuts import render, get_object_or_404
from django.http import FileResponse, Http404
from django.conf import settings
import os
from .models import Category, Product
from cart.forms import CartAddProductForm

def pwa_service_worker(request):
    """Serve service worker from root scope for correct PWA coverage."""
    sw_path = os.path.join(settings.BASE_DIR, 'shop', 'static', 'sw.js')
    if not os.path.exists(sw_path):
        raise Http404
    response = FileResponse(open(sw_path, 'rb'), content_type='application/javascript')
    response['Service-Worker-Allowed'] = '/'
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

def pwa_manifest(request):
    """Serve web app manifest from root."""
    manifest_path = os.path.join(settings.BASE_DIR, 'shop', 'static', 'manifest.json')
    if not os.path.exists(manifest_path):
        raise Http404
    response = FileResponse(open(manifest_path, 'rb'), content_type='application/manifest+json')
    response['Cache-Control'] = 'public, max-age=86400'
    return response

def home(request):
    categories = Category.objects.all()
    featured_products = Product.objects.filter(available=True).order_by('-id')[:20]
    return render(request, 'shop/home.html', {
        'categories': categories,
        'featured_products': featured_products,
    })

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    # Search
    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)
        
    # Price Filtering
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        
    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'query': query
    })

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html', {
        'product': product,
        'cart_product_form': cart_product_form
    })

def about(request):
    return render(request, 'shop/about.html')

def faq(request):
    return render(request, 'shop/faq.html')

def privacy_policy(request):
    return render(request, 'shop/privacy_policy.html')
