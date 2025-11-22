from django.shortcuts import render, get_object_or_404, redirect
from catalog.models import Product, Brand, Category
from customer.models import Customer
from order.models import Order
from .forms import ProductForm, ImageFormSet, SizeFormSet, CustomerBaseForm, CustomerCreateForm
from django.contrib import messages
from django.db.models.deletion import ProtectedError

def admin_dashboard(request):
    total_products = Product.objects.count()
    
    context = {
        'total_products': total_products
    }
    return render(request, 'administrator/admin_dashboard.html', context)

def product_list(request):
    products = Product.objects.all().select_related('brand', 'category')
    return render(request, 'administrator/product/product_list.html', {'products': products})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        image_formset = ImageFormSet(request.POST)
        size_formset = SizeFormSet(request.POST)
        if form.is_valid() and image_formset.is_valid() and size_formset.is_valid():
            product = form.save()
            image_formset.instance = product
            image_formset.save()
            size_formset.instance = product
            size_formset.save()
            return redirect('administrator:product_list')
    else:
        form = ProductForm()
        image_formset = ImageFormSet()
        size_formset = SizeFormSet()
    
    context = {
        'form': form,
        'image_formset': image_formset,
        'size_formset': size_formset
    }
    
    return render(request, 'administrator/product/product_edit.html', context)

def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        image_formset = ImageFormSet(request.POST, instance=product)
        size_formset = SizeFormSet(request.POST, instance=product)
        if form.is_valid() and image_formset.is_valid() and size_formset.is_valid():
            form.save()
            image_formset.save()
            size_formset.save()
            return redirect('administrator:product_list')
    else:
        form = ProductForm(instance=product)
        image_formset = ImageFormSet(instance=product)
        size_formset = SizeFormSet(instance=product)
    
    context = {
        'form': form,
        'image_formset': image_formset,
        'size_formset': size_formset,
        'product': product
    }
    
    return render(request, 'administrator/product/product_edit.html', context)

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    try:
        product.delete()
        messages.success(request, "El producto ha sido eliminado correctamente.")
        
    except ProtectedError as e:
        objetos_bloqueantes = e.args[1]
        ids_pedidos = set(detalle.order.order_id for detalle in objetos_bloqueantes)
        lista_pedidos_str = ", ".join(str(id) for id in ids_pedidos)
        mensaje_error = (
            f"⚠️ No se puede eliminar '{product.name}'. "
            f"Aparece en los siguientes Pedidos (IDs): {lista_pedidos_str} ."
        )
        
        messages.error(request, mensaje_error)
        
    return redirect('administrator:product_list')

def category_list(request):
    categories = Category.objects.all().order_by('name')
    context = {
        'categories': categories
    }
    return render(request, 'administrator/category/category_list.html', context)

def category_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Category.objects.create(name=name)
            return redirect('administrator:category_list')
    return render(request, 'administrator/category/category_edit.html')

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('administrator:category_list')

def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            category.name = name
            category.save()
            return redirect('administrator:category_list')
    context = {
        'category': category
    }
    return render(request, 'administrator/category/category_edit.html', context)

def brand_list(request):
    brands = Brand.objects.all().order_by('name')
    context = {
        'brands': brands
    }
    return render(request, 'administrator/brand/brand_list.html', context)

def brand_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Brand.objects.create(name=name)
            return redirect('administrator:brand_list')
    return render(request, 'administrator/brand/brand_edit.html')

def brand_delete(request, pk):
    brand = get_object_or_404(Brand, pk=pk)
    brand.delete()
    return redirect('administrator:brand_list')

def brand_edit(request, pk):
    brand = get_object_or_404(Brand, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            brand.name = name
            brand.save()
            return redirect('administrator:brand_list')
    context = {
        'brand': brand
    }
    return render(request, 'administrator/brand/brand_edit.html', context)

def customer_list(request):
    customers = Customer.objects.all().order_by('-is_superuser')
    context = {
        'customers': customers
    }
    return render(request, 'administrator/customer/customer_list.html', context)

def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerBaseForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('administrator:customer_list')
    else:
        form = CustomerBaseForm(instance=customer)

    context = {
        'customer': customer,
        'form': form
    }
    return render(request, 'administrator/customer/customer_edit.html', context)

def customer_delete(request, pk):
    if request.user.pk == pk:
        return redirect('administrator:customer_list')
    customer = get_object_or_404(Customer, pk=pk)
    customer.delete()
    return redirect('administrator:customer_list')

def customer_create(request):
    if request.method == 'POST':
        form = CustomerCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('administrator:customer_list')
    else:
        form = CustomerCreateForm()
    context = {
        'form': form
    }
    return render(request, 'administrator/customer/customer_edit.html', context)

def order_list(request):
    orders = Order.objects.all().order_by('-created_at')
    context = {
        'orders': orders
    }
    return render(request, 'administrator/order/order_list.html', context)

def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    context = {
        'order': order
    }
    return render(request, 'administrator/order/order_detail.html', context)

def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.delete()
    return redirect('administrator:order_list')