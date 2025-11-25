from django.shortcuts import render
from catalog.models import Product, Category, Brand, Department

def home(request):
    # Get featured products
    featured_products = Product.objects.filter(
        is_available=True,
        is_featured=True
    ).select_related('brand', 'category').prefetch_related('images')[:8]

    # Get all departments
    departments = Department.objects.all().order_by('order_position', 'name')

    # Get products with offers
    offer_products = Product.objects.filter(
        is_available=True,
        offer_price__isnull=False
    ).select_related('brand', 'category').prefetch_related('images')[:4]

    # Get newest products
    newest_products = Product.objects.filter(
        is_available=True
    ).select_related('brand', 'category').prefetch_related('images').order_by('-created_at')[:4]

    context = {
        'featured_products': featured_products,
        'departments': departments,
        'offer_products': offer_products,
        'newest_products': newest_products,
    }

    return render(request, 'store/home.html', context)

def about(request):
    return render(request, 'store/about.html')