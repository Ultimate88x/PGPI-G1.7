from django import forms
from django.forms import ModelForm, inlineformset_factory
from catalog.models import Product, ProductImage, ProductSize

class ProductImageForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = ProductImage
        fields = ['image', 'is_main', 'order_position']
        widgets = {
            'image': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'URL de la imagen'}),
            'order_position': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 80px'}),
        }

class ProductForm(ModelForm):
    GENDER_CHOICES = [
        ('', 'Seleccionar Género'),
        ('Unisex', 'Unisex'),
        ('Mujer', 'Mujer'),
        ('Hombre', 'Hombre'),
    ]
    
    COLOR_CHOICES = [
        ('', 'Seleccionar Color'),
        ('Varios tonos', 'Varios tonos'),
        ('Varios colores', 'Varios colores'),
        ('Múltiples colores', 'Múltiples colores'),
        ('Negro', 'Negro'),
        ('Blanco', 'Blanco'),
        ('Grisáceo', 'Grisáceo'),
        ('Tonos Cálidos', 'Tonos Cálidos'),
        ('Tonos Rosados', 'Tonos Rosados'),
        ('Tonos Fríos', 'Tonos Fríos'),
    ]
    
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    color = forms.ChoiceField(choices=COLOR_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-select'}))
    
    class Meta:
        model = Product
        fields = ['name', 'brand', 'category', 'price', 'offer_price', 'gender', 'color', 'stock', 'is_available', 'is_featured', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'offer_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'brand': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }
       
ImageFormSet = inlineformset_factory(
    Product, 
    ProductImage, 
    form=ProductImageForm,
    fields=['image'],
    extra=0,
    min_num=1,
    max_num=1,
    can_delete=True,
    widgets={
        'image': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'URL de la imagen'}),
    }
)

SizeFormSet = inlineformset_factory(
    Product, 
    ProductSize,
    fields=['size', 'stock'],
    extra=0,
    can_delete=True,
    widgets={
        'size': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Estándar, 40g, 50ml'}),
        'stock': forms.NumberInput(attrs={'class': 'form-control'}),
    }
)