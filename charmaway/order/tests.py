import pytest
import warnings
from django.urls import reverse
from decimal import Decimal

from order.models import Order, Cart
from catalog.models import Product
from customer.models import Customer


# ------------------------------
# FIXTURES
# ------------------------------

@pytest.fixture(autouse=True)
def suppress_deprecation_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning, module="requests.auth")

@pytest.fixture
def customer(db):
    return Customer.objects.create_user(
        email="cliente@example.com",
        password="password1234",
        name="Juan",
        surnames="Pérez Gómez",
        phone="+34123456789",
        address="Calle Falsa 123",
        city="Madrid",
        zip_code="28001"
    )


@pytest.fixture
def product(db):
    return Product.objects.create(
        name="Producto Test",
        price=Decimal("10.00"),
        stock=20
    )


@pytest.fixture
def cart_item(db, customer, product):
    return Cart.objects.create(
        customer=customer,
        product=product,
        quantity=1,
        current_price=product.price
    )


# ------------------------------
# CART VIEW TESTS
# ------------------------------

def test_view_cart_guest(client, db, product):
    session = client.session
    session["session_key"] = "TESTSESSION"
    session.save()

    Cart.objects.create(
        session_key="TESTSESSION",
        product=product,
        quantity=1,
        current_price=product.price
    )

    url = reverse("view_cart")
    response = client.get(url)
    assert response.status_code == 200
    assert "items" in response.context


def test_view_cart_ajax(client, db, customer, product):
    Cart.objects.create(
        customer=customer,
        product=product,
        quantity=2,
        current_price=product.price
    )

    client.login(email=customer.email, password="password1234")
    url = reverse("view_cart")
    response = client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    assert response.status_code == 200
    assert b"Producto Test" in response.content


# ------------------------------
# CART MODIFY TESTS
# ------------------------------

def test_decrease_from_cart(client, db, cart_item):
    client.login(email=cart_item.customer.email, password="password1234")
    url = reverse("decrease_from_cart", args=[cart_item.product.id])
    response = client.post(url)
    assert response.status_code in [204, 302]

    cart_item_refreshed = Cart.objects.filter(
        customer=cart_item.customer, product=cart_item.product
    ).first()
    assert cart_item_refreshed is None


def test_decrease_removes_item(client, db, customer, product):
    item = Cart.objects.create(
        customer=customer,
        product=product,
        quantity=1,
        current_price=product.price
    )

    client.login(email=customer.email, password="password1234")
    url = reverse("decrease_from_cart", args=[product.id])
    response = client.post(url)
    assert response.status_code in [204, 302]
    assert not Cart.objects.filter(customer=customer, product=product).exists()


def test_remove_from_cart(client, db, cart_item):
    client.login(email=cart_item.customer.email, password="password1234")
    url = reverse("remove_from_cart", args=[cart_item.product.id])
    response = client.post(url)
    assert response.status_code in [204, 302]
    assert not Cart.objects.filter(customer=cart_item.customer, product=cart_item.product).exists()


def test_clear_cart(client, db, customer, product):
    Cart.objects.create(
        customer=customer,
        product=product,
        quantity=1,
        current_price=product.price
    )

    client.login(email=customer.email, password="password1234")
    url = reverse("clear_cart")
    response = client.post(url)
    assert response.status_code in [204, 302]
    assert not Cart.objects.filter(customer=customer).exists()


# ------------------------------
# CHECKOUT TESTS
# ------------------------------

def test_checkout_get(client, db, customer, cart_item):
    client.login(email=customer.email, password="password1234")
    url = reverse("checkout")
    response = client.get(url)
    assert response.status_code == 200
    assert "items" in response.context


def test_checkout_post_cod_redirects(client, db, customer, product):
    Cart.objects.create(
        customer=customer,
        product=product,
        quantity=2,
        current_price=product.price
    )

    client.login(email=customer.email, password="password1234")

    session = client.session
    session['checkout_data'] = {
        "delivery_option": "DELIVERY",
        "address": "Calle Falsa 123",
        "city": "Madrid",
        "zip_code": "28001",
        "email": customer.email,
        "payment_method": "contrarreembolso",
        "notes": ""
    }
    session.save()

    url = reverse("checkout")
    data = {
        "payment_method": "contrarreembolso",
        "delivery_option": "DELIVERY",
        "address": "Calle Falsa 123",
        "city": "Madrid",
        "zip_code": "28001",
        "email": customer.email,
        "notes": ""
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse("payment_success_cod")


# ------------------------------
# PAYMENT TESTS
# ------------------------------

def test_payment_complete_creates_order(client, db, customer, product):
    Cart.objects.create(
        customer=customer,
        product=product,
        quantity=3,
        current_price=product.price
    )

    client.login(email=customer.email, password="password1234")
    session = client.session
    session['checkout_data'] = {
        "delivery_option": "DELIVERY",
        "address": "Calle Falsa 123",
        "city": "Madrid",
        "zip_code": "28001",
        "email": customer.email,
        "payment_method": "CARD",
        "notes": "Test note"
    }
    session.save()

    url = reverse("payment_complete")
    response = client.post(url, {"payment_method": "CARD"})
    assert response.status_code in [200, 302]
    assert Order.objects.filter(customer=customer).exists()


def test_payment_success_cod(client, db, customer):
    session = client.session
    session['checkout_data'] = {
        "delivery_option": "DELIVERY",
        "address": "Calle Falsa 123",
        "city": "Madrid",
        "zip_code": "28001",
        "email": customer.email,
        "payment_method": "COD",
        "notes": ""
    }
    session.save()

    url = reverse("payment_complete")
    response = client.get(url)
    assert response.status_code in [200, 302]


# ------------------------------
# ORDER LOOKUP
# ------------------------------

def test_order_lookup_invalid(client, db):
    url = reverse("order_lookup")
    response = client.post(url, {"order_public_id": "NOEXISTE"})
    assert response.status_code == 200
    assert "error" in response.context
