from django.shortcuts import render
from catalog.models import Product
from .forms import ProductForm, ImageFormSet, SizeFormSet
from django.shortcuts import get_object_or_404, redirect

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
    product.delete()
    return redirect('administrator:product_list')