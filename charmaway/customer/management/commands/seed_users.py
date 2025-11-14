from django.core.management.base import BaseCommand
from customer.models import Customer

class Command(BaseCommand):
    help = 'Crea un admin y un usuario normal de prueba'

    def handle(self, *args, **options):
        if not Customer.objects.filter(email='admin@example.com').exists():
            Customer.objects.create_superuser(
                email='admin@example.com',
                password='SecurePassword',
                name='Wade',
                surnames='Wilson',
                phone='+34123456789',
                address='Calle Admin 1',
                city='Nueva York',
                zip_code='00000'
            )
            self.stdout.write(self.style.SUCCESS('Admin creado correctamente'))

        if not Customer.objects.filter(email='user@example.com').exists():
            Customer.objects.create_user(
                email='user@example.com',
                password='SecurePassword',
                name='Peter',
                surnames='Parker',
                phone='+34111222333',
                address='Ingram Street 20',
                city='Nueva York',
                zip_code='00000'
            )
            self.stdout.write(self.style.SUCCESS('Usuario normal creado correctamente'))
