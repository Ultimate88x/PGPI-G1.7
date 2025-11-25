from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from catalog.models import Category
from .forms import CategoryForm, CustomerCreateForm

User = get_user_model()

class AdminFormTests(TestCase):
    
    """
    PRUEBAS UNITARIAS: Probamos la lógica pura, sin navegador ni servidor.
    """
    
    def test_category_form_no_duplicates(self):
        """Prueba que el CategoryForm no permita nombres repetidos"""
        Category.objects.create(name="Maquillaje")

        form_data = {'name': 'maquillaje'}
        form = CategoryForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_customer_form_validation(self):
        """Prueba que el CustomerForm detecte emails duplicados"""
        User.objects.create_user(
            email='test@gmail.com', 
            password='123',
            name='Usuario',
            surnames='Existente'
        )
        
        form_data = {
            'name': 'Nuevo',
            'surnames': 'Usuario',
            'email': 'test@gmail.com',
            'phone': '123456789',
            'address': 'Calle Falsa 123',
            'city': 'Madrid',
            'zip_code': '28001',
            'is_active': True,
        }
        
        form = CustomerCreateForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn("Este correo electrónico ya está registrado por otro cliente.", str(form.errors))


class AdminSecurityTests(TestCase):
    
    """
    PRUEBAS DE SEGURIDAD: Simulamos peticiones HTTP.
    Probamos que el decorador @admin_required funcione.
    """

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login') 
        
        self.user = User.objects.create_user(
            email='cliente@test.com', 
            password='password123', 
            name='Cliente',
            surnames='Prueba',
            is_superuser=False
        )
        
        self.admin = User.objects.create_superuser(
            email='jefe@test.com', 
            password='password123',
            name='Jefe',
            surnames='Supremo'
        )

    def test_dashboard_redirects_anonymous(self):
        """Un usuario no logueado debe ser redirigido al login"""
        response = self.client.get(reverse('administrator:admin_dashboard'))
        self.assertEqual(response.status_code, 302) 
        self.assertIn(self.login_url, response.url)

    def test_dashboard_redirects_normal_user(self):
        """Un usuario logueado pero NO superuser debe ser expulsado"""
        self.client.login(email='cliente@test.com', password='password123')
        
        response = self.client.get(reverse('administrator:admin_dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_allows_superuser(self):
        """Un superusuario debe ver el dashboard"""
        self.client.login(email='jefe@test.com', password='password123')
        
        response = self.client.get(reverse('administrator:admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'administrator/admin_dashboard.html')


class AdminInterfaceTests(TestCase):
    
    """
    PRUEBAS DE INTERFAZ: Probamos que las vistas hacen lo que deben (Crear, Listar).
    """
    
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(
            email='admin@test.com', 
            password='123',
            name='Admin',
            surnames='Test'
        )
        self.client.force_login(self.admin)

    def test_product_list_view(self):
        """Prueba que la lista de productos carga"""
        from catalog.models import Brand, Product 
        
        c = Category.objects.create(name="Cremas")
        b = Brand.objects.create(name="Nivea")
        p = Product.objects.create(name="Crema Cara", price=10.00, category=c, brand=b)

        response = self.client.get(reverse('administrator:product_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Crema Cara")

    def test_create_category_view(self):
        """Prueba crear una categoría mediante POST"""
        url = reverse('administrator:category_create')
        
        response = self.client.post(url, {
            'name': 'Perfumes'
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Category.objects.filter(name="Perfumes").exists())