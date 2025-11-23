from decimal import Decimal
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Cart, Order, OrderDetail, Product
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


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    session_key = get_session_key(request)

    try:
        quantity = int(request.POST.get("quantity", 1))
    except:
        quantity = 1

    quantity = max(1, quantity)

    if product.stock < quantity:
        return HttpResponse("Not enough stock", status=400)

    if request.user.is_authenticated:
        filter_kwargs = {"customer": request.user, "product": product}
    else:
        filter_kwargs = {"session_key": session_key, "product": product}

    cart_item, created = Cart.objects.get_or_create(
        defaults={"current_price": product.price, "quantity": quantity},
        **filter_kwargs
    )

    if not created:
        if product.stock < quantity:
            return HttpResponse("Not enough stock", status=400)
        cart_item.quantity += quantity

    cart_item.current_price = product.price
    cart_item.save()

    product.stock -= quantity
    product.save()

    return HttpResponse(status=204)


def decrease_from_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    session_key = get_session_key(request)

    if request.user.is_authenticated:
        cart_item = get_object_or_404(Cart, customer=request.user, product=product)
    else:
        cart_item = get_object_or_404(Cart, session_key=session_key, product=product)

    product.stock += 1
    product.save()

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return HttpResponse(status=204)


def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    session_key = get_session_key(request)

    if request.user.is_authenticated:
        cart_item = get_object_or_404(Cart, customer=request.user, product=product)
    else:
        cart_item = get_object_or_404(Cart, session_key=session_key, product=product)

    product.stock += cart_item.quantity
    product.save()

    cart_item.delete()
    return HttpResponse(status=204)


def clear_cart(request):
    if request.user.is_authenticated:
        items = Cart.objects.filter(customer=request.user)
    else:
        items = Cart.objects.filter(session_key=get_session_key(request))

    for item in items:
        item.product.stock += item.quantity
        item.product.save()

    items.delete()
    return HttpResponse(status=204)


def checkout(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            subtotal = Cart.calculate_total(request.user)
        else:
            subtotal = Cart.calculate_total(get_session_key(request))
        shipping = Decimal('0.00') if subtotal > Decimal('20.00') else Decimal('2.99')
        total = subtotal + shipping

        request.session['checkout_total'] = str(total)
        request.session['checkout_data'] = {
            'address': request.POST.get('address'),
            'city': request.POST.get('city'),
            'zip_code': request.POST.get('zip_code'),
            'email': request.POST.get('email'),
            'payment_method': request.POST.get('payment_method'),
            'notes': request.POST.get('notes', ''),
        }

        payment_method = request.POST.get('payment_method')
        if payment_method == 'credit_card':
            return redirect('payment:checkout')
        elif payment_method == 'paypal':
            return redirect('paypal:process_payment')
        else:
            return redirect('payment:checkout')

    return render(request, "checkout.html")


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
    )

    for item in cart_items:
        OrderDetail.objects.create(
            order=order,
            product=item.product,
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
