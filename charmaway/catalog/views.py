from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Product, Category, Brand


def catalog(request):
    """Display catalog with all products, with optional filtering."""
    products = Product.objects.all().select_related('brand', 'category').prefetch_related('images')

    # Get filter parameters
    category_id = request.GET.get('category')
    selected_brands = request.GET.getlist('brand')
    search_query = request.GET.get('q')
    sort_by = request.GET.get('sort', 'name')
    per_page = request.GET.get('per_page', '24')
    price_range = request.GET.get('price_range')
    selected_availability = request.GET.getlist('availability')
    selected_genders = request.GET.getlist('gender')
    selected_colors = request.GET.getlist('color')

    # Apply filters
    if category_id:
        products = products.filter(category_id=category_id)

    if selected_brands:
        products = products.filter(brand_id__in=selected_brands)

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Price range filter
    if price_range:
        if price_range == '0-20':
            products = products.filter(price__lt=20)
        elif price_range == '20-50':
            products = products.filter(price__gte=20, price__lt=50)
        elif price_range == '50-100':
            products = products.filter(price__gte=50, price__lt=100)
        elif price_range == '100-200':
            products = products.filter(price__gte=100, price__lt=200)
        elif price_range == '200+':
            products = products.filter(price__gte=200)

    # Availability filter
    if selected_availability:
        if 'in_stock' in selected_availability and 'out_of_stock' not in selected_availability:
            products = products.filter(stock__gt=0)
        elif 'out_of_stock' in selected_availability and 'in_stock' not in selected_availability:
            products = products.filter(stock=0)

    # Gender filter
    if selected_genders:
        products = products.filter(gender__in=selected_genders)

    # Color filter
    if selected_colors:
        products = products.filter(color__in=selected_colors)

    # Apply sorting
    sort_options = {
        'name': 'name',
        'price_asc': 'price',
        'price_desc': '-price',
        'newest': '-created_at',
        'featured': '-is_featured'
    }
    products = products.order_by(sort_options.get(sort_by, 'name'))

    # Pagination
    try:
        items_per_page = int(per_page)
        if items_per_page not in [24, 36, 48]:
            items_per_page = 24
    except (ValueError, TypeError):
        items_per_page = 24

    paginator = Paginator(products, items_per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Get all categories and brands for filters
    categories = Category.objects.all().order_by('name')
    brands = Brand.objects.all().order_by('name')

    # Get available colors from products
    available_colors = Product.objects.all().values_list('color', flat=True).distinct().order_by('color')
    available_colors = [color for color in available_colors if color]  # Remove None values

    context = {
        'products': page_obj,
        'page_obj': page_obj,
        'categories': categories,
        'brands': brands,
        'selected_category': category_id,
        'selected_brands': selected_brands,
        'search_query': search_query,
        'sort_by': sort_by,
        'per_page': per_page,
        'selected_price_range': price_range,
        'selected_availability': selected_availability,
        'selected_genders': selected_genders,
        'selected_colors': selected_colors,
        'available_colors': available_colors,
    }

    return render(request, 'catalog/catalog.html', context)


def product_detail(request, product_id):
    """Display detailed information about a specific product."""
    product = get_object_or_404(
        Product.objects.select_related('brand', 'category').prefetch_related('images', 'sizes'),
        id=product_id
    )

    # Get main image or first image
    main_image = product.images.filter(is_main=True).first()
    if not main_image:
        main_image = product.images.first()

    # Get all images
    images = product.images.all().order_by('order_position')

    # Get available sizes
    sizes = product.sizes.all().order_by('size')

    context = {
        'product': product,
        'main_image': main_image,
        'images': images,
        'sizes': sizes,
    }

    return render(request, 'catalog/product_detail.html', context)


def category_list(request, category_id):
    """Display products filtered by category."""
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(
        category=category
    ).select_related('brand', 'category').prefetch_related('images')

    context = {
        'category': category,
        'products': products,
    }

    return render(request, 'catalog/category.html', context)


def brand_list(request, brand_id):
    """Display products filtered by brand."""
    brand = get_object_or_404(Brand, id=brand_id)
    products = Product.objects.filter(
        brand=brand
    ).select_related('brand', 'category').prefetch_related('images')

    context = {
        'brand': brand,
        'products': products,
    }

    return render(request, 'catalog/brand.html', context)
