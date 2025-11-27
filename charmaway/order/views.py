from decimal import Decimal
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Cart, Order, OrderDetail, Product, DeliveryOption
from services.models import Service
from charmaway.utils.mailjet_api import send_mail_via_mailjet
import threading



def get_session_key(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def get_cart_queryset(request):
    if request.user.is_authenticated:
        return Cart.objects.filter(customer=request.user)
    else:
        return Cart.objects.filter(session_key=get_session_key(request))


def view_cart(request):
    if request.user.is_authenticated:
        user_or_session = request.user
    else:
        user_or_session = get_session_key(request)

    items = get_cart_queryset(request)
    subtotal = Cart.calculate_total(user_or_session)
    shipping = Decimal('0.00') if subtotal > Decimal('20.00') else Decimal('2.99')
    total = subtotal + shipping

    if request.GET.get("ajax"):
        return render(request, "cart_dropdown.html", {
            "items": items,
            "subtotal": subtotal,
            "shipping": shipping,
            "total": total,
        })

    return render(request, "cart.html", {
        "items": items,
        "subtotal": subtotal,
        "shipping": shipping,
        "total": total,
    })


def add_product_to_cart(request, product_id):
    session_key = get_session_key(request)
    product = get_object_or_404(Product, pk=product_id)

    try:
        quantity = int(request.POST.get("quantity", 1))
    except:
        quantity = 1

    quantity = max(1, quantity)

    if product.stock < quantity:
        return HttpResponse("Not enough stock", status=400)

    if request.user.is_authenticated:
        filter_kwargs = {"customer": request.user, "product": product, "service": None}
    else:
        filter_kwargs = {"session_key": session_key, "product": product, "service": None}

    cart_item, created = Cart.objects.get_or_create(
        defaults={"current_price": product.price, "quantity": quantity},
        **filter_kwargs
    )

    if not created:
        cart_item.quantity += quantity

    cart_item.current_price = product.price
    cart_item.save()

    product.stock -= quantity
    product.save()

    return HttpResponse(status=204)


def add_service_to_cart(request, service_id):
    session_key = get_session_key(request)
    service = get_object_or_404(Service, pk=service_id)
    final_price = service.get_final_price()

    try:
        quantity = int(request.POST.get("quantity", 1))
    except:
        quantity = 1

    quantity = max(1, quantity)

    if request.user.is_authenticated:
        filter_kwargs = {"customer": request.user, "product": None, "service": service}
    else:
        filter_kwargs = {"session_key": session_key, "product": None, "service": service}

    cart_item, created = Cart.objects.get_or_create(
        defaults={"current_price": final_price, "quantity": quantity},
        **filter_kwargs
    )

    if not created:
        cart_item.quantity += quantity

    cart_item.current_price = final_price
    cart_item.save()

    return HttpResponse(status=204)


def decrease_product_from_cart(request, product_id):
    session_key = get_session_key(request)
    product = get_object_or_404(Product, pk=product_id)

    if request.user.is_authenticated:
        cart_item = get_object_or_404(Cart, customer=request.user, product=product, service=None)
    else:
        cart_item = get_object_or_404(Cart, session_key=session_key, product=product, service=None)

    product.stock += 1
    product.save()

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return HttpResponse(status=204)


def decrease_service_from_cart(request, service_id):
    session_key = get_session_key(request)
    service = get_object_or_404(Service, pk=service_id)

    if request.user.is_authenticated:
        cart_item = get_object_or_404(Cart, customer=request.user, product=None, service=service)
    else:
        cart_item = get_object_or_404(Cart, session_key=session_key, product=None, service=service)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return HttpResponse(status=204)


def remove_product_from_cart(request, product_id):
    session_key = get_session_key(request)
    product = get_object_or_404(Product, pk=product_id)

    if request.user.is_authenticated:
        cart_item = get_object_or_404(Cart, customer=request.user, product=product, service=None)
    else:
        cart_item = get_object_or_404(Cart, session_key=session_key, product=product, service=None)

    product.stock += cart_item.quantity
    product.save()

    cart_item.delete()
    return HttpResponse(status=204)


def remove_service_from_cart(request, service_id):
    session_key = get_session_key(request)
    service = get_object_or_404(Service, pk=service_id)

    if request.user.is_authenticated:
        cart_item = get_object_or_404(Cart, customer=request.user, product=None, service=service)
    else:
        cart_item = get_object_or_404(Cart, session_key=session_key, product=None, service=service)

    cart_item.delete()
    return HttpResponse(status=204)


def clear_cart(request):
    if request.user.is_authenticated:
        items = Cart.objects.filter(customer=request.user)
    else:
        items = Cart.objects.filter(session_key=get_session_key(request))

    for item in items:
        if item.product:
            item.product.stock += item.quantity
            item.product.save()

    items.delete()
    return HttpResponse(status=204)


def checkout(request):
    if request.user.is_authenticated:
        user_or_session = request.user
    else:
        user_or_session = get_session_key(request)

    items = get_cart_queryset(request)

    if not items.exists():
        return redirect('view_cart')

    subtotal = Cart.calculate_total(user_or_session)
    shipping = Decimal('0.00') if subtotal > Decimal('20.00') else Decimal('2.99')
    total = subtotal + shipping

    if request.method == "POST":
        request.session['checkout_total'] = str(total)
        request.session['checkout_data'] = {
            'address': request.POST.get('address'),
            'city': request.POST.get('city'),
            'zip_code': request.POST.get('zip_code'),
            'email': request.POST.get('email'),
            'payment_method': request.POST.get('payment_method'),
            'notes': request.POST.get('notes', ''),
            'delivery_option': request.POST.get('delivery_option'),
        }

        payment_method = request.POST.get('payment_method', '').lower()

        if payment_method == 'tarjeta_credito':
            return redirect('payment:checkout')
        elif payment_method == 'contrarreembolso':
            return redirect('payment_success_cod')
        else:
            return redirect('view_cart') 

    return render(request, "checkout.html", {
        "items": items,
        "subtotal": subtotal,
        "shipping": shipping,
        "total": total
    })

def buy_now_product(request, product_id):

    clear_cart(request)

    add_product_to_cart(request, product_id)

    response = checkout(request)

    return response

def buy_now_service(request, service_id):

    clear_cart(request)

    add_service_to_cart(request, service_id)

    response = checkout(request)

    return response


def order_detail(request, public_id):
    order = get_object_or_404(Order, public_id=public_id)
    return render(request, "order_detail.html", {"order": order})


def order_lookup(request):
    context = {}

    if request.method == "POST":
        order_public_id = request.POST.get("order_public_id")
        if order_public_id:
            try:
                order = Order.objects.get(public_id=order_public_id)
                return redirect('order_detail', public_id=order.public_id)
            except Order.DoesNotExist:
                context['error'] = "Pedido no encontrado."

    return render(request, "order_lookup.html", context)


def send_email_async(subject, plain_message, from_email, recipient_list, html_message=None):
    threading.Thread(
        target=send_mail,
        args=(subject, plain_message, from_email, recipient_list),
        kwargs={'html_message': html_message, 'fail_silently': False}
    ).start()


def payment_complete_view(request):
    cart_items = get_cart_queryset(request)
    checkout_data = request.session.get('checkout_data')
    delivery_option = checkout_data.get("delivery_option")

    if not checkout_data:
        return redirect("view_cart")

    if not cart_items.exists():
        return redirect("view_cart")
    
    if request.user.is_authenticated:
        subtotal = Cart.calculate_total(request.user)
    else:
        subtotal = Cart.calculate_total(get_session_key(request))

    if delivery_option == DeliveryOption.DELIVERY:
        shipping = 0 if subtotal > 20 else 2.99
    else:
        shipping = 0

    order = Order.objects.create(
        customer=request.user if request.user.is_authenticated else None,
        address=checkout_data['address'],
        city=checkout_data['city'],
        zip_code=checkout_data['zip_code'],
        email=checkout_data['email'],
        payment_method=checkout_data['payment_method'],
        notes=checkout_data.get('notes', ''),
        shipping_cost=shipping,
        delivery_option=delivery_option,
    )

    for item in cart_items:
        OrderDetail.objects.create(
            order=order,
            product=item.product if item.product else None,
            service=item.service if item.service else None,
            quantity=item.quantity,
            unit_price=item.current_price,
            subtotal=item.quantity * item.current_price
        )

    order.calculate_total()
    order.save()

    cart_items.delete()
    del request.session['checkout_data']
    request.session['order_id_to_pay'] = order.order_id

    subject = f"Confirmación de pedido #{order.public_id}"
    html_message = render_to_string("order_success_for_mail.html", {
        "order": order,
        "user": request.user,
    })
    threading.Thread(
        target=send_mail_via_mailjet,
        args=(subject, html_message, [order.email])
    ).start()

    return render(request, "order_success.html", {"order": order})


def payment_success_cod(request):
    cart_items = get_cart_queryset(request)
    checkout_data = request.session.get('checkout_data')
    delivery_option = checkout_data.get("delivery_option")

    if not checkout_data:
        return redirect("view_cart")

    if not cart_items.exists():
        return redirect("view_cart")

    if request.user.is_authenticated:
        subtotal = Cart.calculate_total(request.user)
    else:
        subtotal = Cart.calculate_total(get_session_key(request))

    shipping = 0 if subtotal > 20 else 2.99

    order = Order.objects.create(
        customer=request.user if request.user.is_authenticated else None,
        address=checkout_data['address'],
        city=checkout_data['city'],
        zip_code=checkout_data['zip_code'],
        email=checkout_data['email'],
        payment_method=checkout_data['payment_method'],
        notes=checkout_data.get('notes', ''),
        shipping_cost=shipping,
        delivery_option=delivery_option,
    )

    for item in cart_items:
        OrderDetail.objects.create(
            order=order,
            product=item.product if item.product else None,
            service=item.service if item.service else None,
            quantity=item.quantity,
            unit_price=item.current_price,
            subtotal=item.quantity * item.current_price
        )

    order.calculate_total()
    order.save()

    cart_items.delete()
    del request.session['checkout_data']

    subject = f"Pedido a contrarreembolso #{order.public_id}"
    html_message = render_to_string("order_success_cod_mail.html", {
        "order": order
    })
    threading.Thread(
        target=send_mail_via_mailjet,
        args=(subject, html_message, [order.email])
    ).start()

    return render(request, "order_success_cod.html", {"order": order})