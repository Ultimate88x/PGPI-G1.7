from django.core.management.base import BaseCommand
from customer.models import Customer
from catalog.models import Product
from order.models import Cart, Order, OrderDetail
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

        # Limpiar datos
        Cart.objects.all().delete()
        OrderDetail.objects.all().delete()
        Order.objects.all().delete()

        fake_streets = [
            "Calle Mayor", "Avenida del Sol", "Paseo de la Luna",
            "Calle Jardines", "Calle Nueva", "Avenida Castilla",
            "Paseo del Río"
        ]

        cities = ["Madrid", "Barcelona", "Sevilla", "Valencia", "Bilbao", "Málaga"]

        for customer in customers:

            cart_count = random.randint(1, 5)
            cart_products = random.sample(products, k=cart_count)

            for product in cart_products:
                Cart.objects.create(
                    customer=customer,
                    product=product,
                    quantity=random.randint(1, 3),
                    current_price=product.price
                )

            order_count = random.randint(1, 3)

            for _ in range(order_count):

                address_text = f"{random.choice(fake_streets)} {random.randint(1, 200)}"
                city = random.choice(cities)
                zip_code = f"{random.randint(10000, 99999)}"

                order = Order.objects.create(
                    customer=customer,
                    email=customer.email,
                    address=address_text,
                    city=city,
                    zip_code=zip_code,
                    shipping_cost=Decimal('5.00'),
                    payment_method=random.choice(['credit_card', 'paypal']),
                )

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
