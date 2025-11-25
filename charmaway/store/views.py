from django.shortcuts import render
from catalog.models import Product, Category, Brand, Department

def home(request):
    # Get featured products
    featured_products = Product.objects.exclude(
        category__department__name='Servicios'
    ).filter(
        is_available=True,
        is_featured=True
    ).select_related('brand', 'category').prefetch_related('images')[:8]

    # Get all departments
    departments = Department.objects.all().order_by('order_position', 'name')

    context = {
        'featured_products': featured_products,
        'departments': departments,
    }

    return render(request, 'store/home.html', context)

def about(request):
    return render(request, 'store/about.html')