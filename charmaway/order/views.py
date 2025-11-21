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
    items = get_cart_queryset(request)

    for item in items:
        item.subtotal = item.quantity * item.current_price

    total = sum(item.subtotal for item in items)

    if request.GET.get("ajax"):
        return render(request, "cart_dropdown.html", {
            "items": items,
            "total": total
        })

    return render(request, "cart.html", {
        "items": items,
        "total": total
    })


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    session_key = get_session_key(request)

    try:
        quantity = int(request.POST.get("quantity", 1))
    except:
        quantity = 1

    quantity = max(1, quantity)

    if request.user.is_authenticated:
        filter_kwargs = {"customer": request.user, "product": product}
        defaults = {"current_price": product.price, "quantity": quantity}
    else:
        filter_kwargs = {"session_key": session_key, "product": product}
        defaults = {"current_price": product.price, "quantity": quantity}

    cart_item, created = Cart.objects.get_or_create(
        defaults=defaults,
        **filter_kwargs
    )

    if not created:
        cart_item.quantity += quantity

    cart_item.current_price = product.price
    cart_item.save()

    return HttpResponse(status=204)


def decrease_from_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    session_key = get_session_key(request)

    if request.user.is_authenticated:
        cart_item = get_object_or_404(Cart, customer=request.user, product=product)
    else:
        cart_item = get_object_or_404(Cart, session_key=session_key, product=product)

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

    cart_item.delete()
    return HttpResponse(status=204)


def clear_cart(request):
    if request.user.is_authenticated:
        Cart.objects.filter(customer=request.user).delete()
    else:
        Cart.objects.filter(session_key=get_session_key(request)).delete()
    return HttpResponse(status=204)


def checkout(request):
    session_key = get_session_key(request)
    cart_items = get_cart_queryset(request)

    address = None
    city = None
    zip_code = None
    email = None

    if request.method == "POST":
        address = request.POST.get('address')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip_code')
        email = request.POST.get('email')

        order = Order.objects.create(
            customer=request.user if request.user.is_authenticated else None,
            address=address,
            city=city,
            zip_code=zip_code,
            email=email,
            payment_method=request.POST.get('payment_method'),
            notes=request.POST.get('notes', '')
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

        request.session['order_id_to_pay'] = order.order_id
        cart_items.delete()

        if order.payment_method == 'credit_card':
            return redirect('payment:checkout')
        elif order.payment_method == 'paypal':
            return redirect('paypal:process_payment')
        else:
            return redirect('payment:checkout')

    return render(request, "checkout.html", {
        "cart_items": cart_items,
        "total": Cart.calculate_total(request.user if request.user.is_authenticated else session_key)
    })


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
    order_id = request.session.get('order_id_to_pay')

    if not order_id:
        return redirect("view_cart")

    try:
        order = Order.objects.get(order_id=order_id)

        subject = f"Confirmación de pedido #{order.order_id}"
        html_message = render_to_string("order_success_for_mail.html", {
            "order": order,
            "user": request.user,
        })

        threading.Thread(
            target=send_mail_via_mailjet,
            args=(subject, html_message, [order.email])
        ).start()

        return render(request, "order_success.html", {"order": order})

    except Order.DoesNotExist:
        return redirect("view_cart")
