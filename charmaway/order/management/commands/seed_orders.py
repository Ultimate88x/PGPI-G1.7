from django.core.management.base import BaseCommand
from customer.models import Customer
from catalog.models import Product
from order.models import Cart, Order, OrderDetail, OrderStatus
from decimal import Decimal
import shortuuid


class Command(BaseCommand):
    help = 'Crea pedidos y carritos fijos para pruebas con todos los clientes'

    def handle(self, *args, **options):
        def calculate_shipping(subtotal):
            return Decimal('2.99') if subtotal > Decimal('20.00') else Decimal('0.00')

        customers = list(Customer.objects.all()[:7])

        products = list(Product.objects.filter(is_available=True)[:5])
        
        p1, p2, p3, p4, p5 = products
        admin, user, c1, c2, c3, c4, c5 = customers

        Cart.objects.all().delete()
        OrderDetail.objects.all().delete()
        Order.objects.all().delete()

        Cart.objects.create(customer=admin, product=p1, quantity=1, current_price=p1.price)
        Cart.objects.create(customer=user, product=p2, quantity=2, current_price=p2.price)
        Cart.objects.create(customer=c1, product=p3, quantity=1, current_price=p3.price)
        Cart.objects.create(customer=c2, product=p4, quantity=2, current_price=p4.price)
        Cart.objects.create(customer=c3, product=p5, quantity=1, current_price=p5.price)
        Cart.objects.create(customer=c4, product=p1, quantity=3, current_price=p1.price)
        Cart.objects.create(customer=c5, product=p2, quantity=2, current_price=p2.price)

        self.stdout.write(self.style.SUCCESS('Carritos fijos creados'))

        o1 = Order.objects.create(
            public_id=shortuuid.uuid()[:12], customer=admin, email=admin.email,
            address=admin.address, city=admin.city, zip_code=admin.zip_code,
            payment_method='credit_card', status=OrderStatus.PROCESSING
        )
        OrderDetail.objects.create(order=o1, product=p1, quantity=1, unit_price=p1.price, subtotal=p1.price)
        o1.subtotal = p1.price
        o1.shipping_cost = calculate_shipping(o1.subtotal)
        o1.final_price = o1.subtotal + o1.shipping_cost
        o1.save()

        o2 = Order.objects.create(
            public_id=shortuuid.uuid()[:12], customer=user, email=user.email,
            address=user.address, city=user.city, zip_code=user.zip_code,
            payment_method='paypal', status=OrderStatus.SHIPPED
        )
        OrderDetail.objects.create(order=o2, product=p2, quantity=2, unit_price=p2.price, subtotal=p2.price*2)
        o2.subtotal = p2.price*2
        o2.shipping_cost = calculate_shipping(o2.subtotal)
        o2.final_price = o2.subtotal + o2.shipping_cost
        o2.save()

        o3 = Order.objects.create(
            public_id=shortuuid.uuid()[:12], customer=c1, email=c1.email,
            address=c1.address, city=c1.city, zip_code=c1.zip_code,
            payment_method='credit_card', status=OrderStatus.DELIVERED
        )
        OrderDetail.objects.create(order=o3, product=p1, quantity=1, unit_price=p1.price, subtotal=p1.price)
        OrderDetail.objects.create(order=o3, product=p3, quantity=1, unit_price=p3.price, subtotal=p3.price)
        o3.subtotal = p1.price + p3.price
        o3.shipping_cost = calculate_shipping(o3.subtotal)
        o3.final_price = o3.subtotal + o3.shipping_cost
        o3.save()

        o4 = Order.objects.create(
            public_id=shortuuid.uuid()[:12], customer=c1, email=c1.email,
            address='Calle Mayor 12', city=c1.city, zip_code=c1.zip_code,
            payment_method='paypal', status=OrderStatus.CANCELLED
        )
        OrderDetail.objects.create(order=o4, product=p2, quantity=1, unit_price=p2.price, subtotal=p2.price)
        OrderDetail.objects.create(order=o4, product=p4, quantity=1, unit_price=p4.price, subtotal=p4.price)
        o4.subtotal = p2.price + p4.price
        o4.shipping_cost = calculate_shipping(o4.subtotal)
        o4.final_price = o4.subtotal + o4.shipping_cost
        o4.save()

        o_extra1 = Order.objects.create(
            public_id=shortuuid.uuid()[:12], customer=c1, email=c1.email,
            address='Av. Nueva 45', city=c1.city, zip_code=c1.zip_code,
            payment_method='credit_card', status=OrderStatus.PROCESSING
        )
        OrderDetail.objects.create(order=o_extra1, product=p5, quantity=2, unit_price=p5.price, subtotal=p5.price*2)
        o_extra1.subtotal = p5.price*2
        o_extra1.shipping_cost = calculate_shipping(o_extra1.subtotal)
        o_extra1.final_price = o_extra1.subtotal + o_extra1.shipping_cost
        o_extra1.save()

        o_extra2 = Order.objects.create(
            public_id=shortuuid.uuid()[:12], customer=c1, email=c1.email,
            address='Calle del Río 10', city=c1.city, zip_code=c1.zip_code,
            payment_method='paypal', status=OrderStatus.SHIPPED
        )
        OrderDetail.objects.create(order=o_extra2, product=p3, quantity=1, unit_price=p3.price, subtotal=p3.price)
        OrderDetail.objects.create(order=o_extra2, product=p4, quantity=2, unit_price=p4.price, subtotal=p4.price*2)
        o_extra2.subtotal = p3.price + p4.price*2
        o_extra2.shipping_cost = calculate_shipping(o_extra2.subtotal)
        o_extra2.final_price = o_extra2.subtotal + o_extra2.shipping_cost
        o_extra2.save()

        o5 = Order.objects.create(
            public_id=shortuuid.uuid()[:12], customer=c2, email=c2.email,
            address=c2.address, city=c2.city, zip_code=c2.zip_code,
            payment_method='credit_card', status=OrderStatus.DELIVERED
        )
        OrderDetail.objects.create(order=o5, product=p1, quantity=2, unit_price=p1.price, subtotal=p1.price*2)
        o5.subtotal = p1.price*2
        o5.shipping_cost = calculate_shipping(o5.subtotal)
        o5.final_price = o5.subtotal + o5.shipping_cost
        o5.save()

        o6 = Order.objects.create(
            public_id=shortuuid.uuid()[:12], customer=c2, email=c2.email,
            address='Avenida Reina Mercedes 130', city=c2.city, zip_code=c2.zip_code,
            payment_method='paypal', status=OrderStatus.PROCESSING
        )
        OrderDetail.objects.create(order=o6, product=p3, quantity=1, unit_price=p3.price, subtotal=p3.price)
        OrderDetail.objects.create(order=o6, product=p4, quantity=1, unit_price=p4.price, subtotal=p4.price)
        o6.subtotal = p3.price + p4.price
        o6.shipping_cost = calculate_shipping(o6.subtotal)
        o6.final_price = o6.subtotal + o6.shipping_cost
        o6.save()

        o7 = Order.objects.create(
            public_id=shortuuid.uuid()[:12], customer=c3, email=c3.email,
            address=c3.address, city=c3.city, zip_code=c3.zip_code,
            payment_method='credit_card', status=OrderStatus.CANCELLED
        )
        OrderDetail.objects.create(order=o7, product=p1, quantity=1, unit_price=p1.price, subtotal=p1.price)
        o7.subtotal = p1.price
        o7.shipping_cost = calculate_shipping(o7.subtotal)
        o7.final_price = o7.subtotal + o7.shipping_cost
        o7.save()

        o8 = Order.objects.create(
            public_id=shortuuid.uuid()[:12], customer=c3, email=c3.email,
            address='Paseo de la Luna 18', city=c3.city, zip_code=c3.zip_code,
            payment_method='paypal', status=OrderStatus.SHIPPED
        )
        OrderDetail.objects.create(order=o8, product=p2, quantity=2, unit_price=p2.price, subtotal=p2.price*2)
        o8.subtotal = p2.price*2
        o8.shipping_cost = calculate_shipping(o8.subtotal)
        o8.final_price = o8.subtotal + o8.shipping_cost
        o8.save()

        o9 = Order.objects.create(
            public_id=shortuuid.uuid()[:12], customer=c4, email=c4.email,
            address=c4.address, city=c4.city, zip_code=c4.zip_code,
            payment_method='credit_card', status=OrderStatus.PROCESSING
        )
        OrderDetail.objects.create(order=o9, product=p3, quantity=1, unit_price=p3.price, subtotal=p3.price)
        o9.subtotal = p3.price
        o9.shipping_cost = calculate_shipping(o9.subtotal)
        o9.final_price = o9.subtotal + o9.shipping_cost
        o9.save()

        o10 = Order.objects.create(
            public_id=shortuuid.uuid()[:12], customer=c4, email=c4.email,
            address='Ronda del Río 25', city=c4.city, zip_code=c4.zip_code,
            payment_method='paypal', status=OrderStatus.DELIVERED
        )
        OrderDetail.objects.create(order=o10, product=p4, quantity=1, unit_price=p4.price, subtotal=p4.price)
        OrderDetail.objects.create(order=o10, product=p5, quantity=1, unit_price=p5.price, subtotal=p5.price)
        o10.subtotal = p4.price + p5.price
        o10.shipping_cost = calculate_shipping(o10.subtotal)
        o10.final_price = o10.subtotal + o10.shipping_cost
        o10.save()

        o11 = Order.objects.create(
            public_id=shortuuid.uuid()[:12], customer=c5, email=c5.email,
            address=c5.address, city=c5.city, zip_code=c5.zip_code,
            payment_method='credit_card', status=OrderStatus.PROCESSING
        )
        OrderDetail.objects.create(order=o11, product=p1, quantity=1, unit_price=p1.price, subtotal=p1.price)
        OrderDetail.objects.create(order=o11, product=p5, quantity=1, unit_price=p5.price, subtotal=p5.price)
        o11.subtotal = p1.price + p5.price
        o11.shipping_cost = calculate_shipping(o11.subtotal)
        o11.final_price = o11.subtotal + o11.shipping_cost
        o11.save()

        o12 = Order.objects.create(
            public_id=shortuuid.uuid()[:12], customer=c5, email=c5.email,
            address='Calle del Sol 105', city=c5.city, zip_code=c5.zip_code,
            payment_method='paypal', status=OrderStatus.SHIPPED
        )
        OrderDetail.objects.create(order=o12, product=p2, quantity=2, unit_price=p2.price, subtotal=p2.price*2)
        o12.subtotal = p2.price*2
        o12.shipping_cost = calculate_shipping(o12.subtotal)
        o12.final_price = o12.subtotal + o12.shipping_cost
        o12.save()

        self.stdout.write(self.style.SUCCESS('✔ Pedidos y carritos fijos creados para todos los clientes con estados variados'))
