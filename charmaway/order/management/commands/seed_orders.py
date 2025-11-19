from django.core.management.base import BaseCommand
from customer.models import Customer
from catalog.models import Product
from order.models import Cart, Order, OrderDetail, Address
import random
from decimal import Decimal

class Command(BaseCommand):
    help = 'Seed the database with orders and carts'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding orders and carts...')

        customers = Customer.objects.all()
        products = list(Product.objects.filter(is_available=True))

        if not customers or not products:
            self.stdout.write(self.style.ERROR('No hay clientes o productos para crear orders/carts'))
            return

        # Vaciar carritos y pedidos existentes
        Cart.objects.all().delete()
        OrderDetail.objects.all().delete()
        Order.objects.all().delete()

        for customer in customers:
            # Crear carrito con 1-5 productos aleatorios
            cart_count = random.randint(1, 5)
            cart_products = random.sample(products, k=cart_count)
            for product in cart_products:
                Cart.objects.create(
                    customer=customer,
                    product=product,
                    quantity=random.randint(1, 3),
                    current_price=product.price
                )

            # Crear 1-3 pedidos
            order_count = random.randint(1, 3)
            addresses = list(customer.addresses.all())
            if not addresses:
                self.stdout.write(self.style.WARNING(f'Cliente {customer.email} no tiene direcciones, saltando pedido'))
                continue

            for _ in range(order_count):
                address = random.choice(addresses)
                order = Order.objects.create(
                    customer=customer,
                    shipping_address=address,
                    shipping_cost=Decimal('5.00'),
                    payment_method=random.choice(['Credit Card', 'PayPal', 'Bank Transfer']),
                )

                # Agregar 1-4 productos al pedido
                order_products = random.sample(products, k=random.randint(1, 4))
                subtotal = Decimal('0.00')
                for product in order_products:
                    quantity = random.randint(1, 3)
                    detail = OrderDetail.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        unit_price=product.price,
                        subtotal=Decimal(product.price) * quantity
                    )
                    subtotal += detail.subtotal

                order.subtotal = subtotal
                order.final_price = subtotal + order.shipping_cost
                order.save()

        self.stdout.write(self.style.SUCCESS('Orders and carts seeded successfully!'))
