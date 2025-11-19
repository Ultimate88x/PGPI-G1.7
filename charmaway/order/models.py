from django.db import models
from django.utils import timezone
from customer.models import Customer
from catalog.models import Product


class Address(models.Model):
    address_id = models.AutoField(primary_key=True)

    user = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="addresses",
        null=True,
        blank=True
    )

    street = models.CharField(max_length=255)
    number = models.CharField(max_length=20)
    floor = models.CharField(max_length=20, blank=True, null=True)
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    is_default = models.BooleanField(default=False)

    def set_default(self):
        if self.user:
            Address.objects.filter(user=self.user).update(is_default=False)
        self.is_default = True
        self.save()

    def __str__(self):
        return f"{self.street} {self.number}, {self.city}"


class OrderStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    PROCESSING = "PROCESSING", "Processing"
    SHIPPED = "SHIPPED", "Shipped"
    DELIVERED = "DELIVERED", "Delivered"
    CANCELLED = "CANCELLED", "Cancelled"


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="orders",
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(default=timezone.now)

    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING
    )

    shipping_address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT
    )

    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    payment_method = models.CharField(max_length=50)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True)

    def change_status(self, new_status):
        self.status = new_status
        self.save()

    def calculate_total(self):
        details = self.details.all()
        self.subtotal = sum(d.subtotal for d in details)
        self.final_price = self.subtotal + self.shipping_cost
        self.save()

    def cancel(self):
        self.status = OrderStatus.CANCELLED
        self.save()

    def get_details(self):
        return self.details.all()

    def __str__(self):
        customer_name = self.customer.name if self.customer else "Anonymous"
        return f"Order #{self.order_id} - {customer_name}"


class OrderDetail(models.Model):
    detail_id = models.AutoField(primary_key=True)

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="details"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )

    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def calculate_subtotal(self):
        self.subtotal = self.unit_price * self.quantity
        self.save()

    def __str__(self):
        return f"{self.quantity} x {self.product}"


class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="cart_items",
        null=True,
        blank=True
    )

    session_key = models.CharField(max_length=40, null=True, blank=True)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(default=timezone.now)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)

    def add_product(self, amount=1):
        self.quantity += amount
        self.save()

    def update_quantity(self, quantity):
        self.quantity = max(1, quantity)
        self.save()

    def remove_product(self):
        self.delete()

    @staticmethod
    def clear_cart(user_or_session):
        if isinstance(user_or_session, Customer):
            Cart.objects.filter(customer=user_or_session).delete()
        else:
            Cart.objects.filter(session_key=user_or_session).delete()

    @staticmethod
    def calculate_total(user_or_session):
        if isinstance(user_or_session, Customer):
            items = Cart.objects.filter(customer=user_or_session)
        else:
            items = Cart.objects.filter(session_key=user_or_session)

        return sum(item.current_price * item.quantity for item in items)

    def __str__(self):
        owner = self.customer.name if self.customer else f"Session {self.session_key}"
        return f"{self.quantity} x {self.product} (Owner: {owner})"
