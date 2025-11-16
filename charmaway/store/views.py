from django.shortcuts import render
from catalog.models import Product, Category, Brand

def home(request):
    # Get featured products
    featured_products = Product.objects.filter(
        is_available=True,
        is_featured=True
    ).select_related('brand', 'category').prefetch_related('images')[:8]

    # Get all categories
    categories = Category.objects.all()

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
        'categories': categories,
        'offer_products': offer_products,
        'newest_products': newest_products,
    }

    return render(request, 'store/home.html', context)