from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Cart, Order, OrderDetail, Address, Product


def get_session_key(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def get_cart_queryset(request):
    """
    Devuelve el queryset del carrito dependiendo si el usuario está logueado
    o es un visitante anónimo.
    """
    if request.user.is_authenticated:
        return Cart.objects.filter(customer=request.user)
    else:
        return Cart.objects.filter(session_key=get_session_key(request))


def view_cart(request):
    items = get_cart_queryset(request)

    total = 0
    for item in items:
        item.subtotal = item.quantity * item.current_price
        total += item.subtotal

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

    return redirect("view_cart")


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

    return redirect("view_cart")


def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    session_key = get_session_key(request)

    if request.user.is_authenticated:
        cart_item = get_object_or_404(Cart, customer=request.user, product=product)
    else:
        cart_item = get_object_or_404(Cart, session_key=session_key, product=product)

    cart_item.delete()
    return redirect("view_cart")


def clear_cart(request):
    if request.user.is_authenticated:
        Cart.objects.filter(customer=request.user).delete()
    else:
        Cart.objects.filter(session_key=get_session_key(request)).delete()
    return redirect("view_cart")


def checkout(request):
    session_key = get_session_key(request)

    cart_items = get_cart_queryset(request)

    if not cart_items.exists():
        return redirect("view_cart")

    default_address = None
    if request.user.is_authenticated:
        default_address = Address.objects.filter(user=request.user, is_default=True).first()

    if request.method == "POST":

        if default_address:
            shipping_address = default_address
        else:
            shipping_address = Address.objects.create(
                user=request.user if request.user.is_authenticated else None,
                street=request.POST.get('street'),
                number=request.POST.get('number'),
                floor=request.POST.get('floor'),
                postal_code=request.POST.get('postal_code'),
                city=request.POST.get('city'),
                state=request.POST.get('state'),
                country=request.POST.get('country'),
            )

        order = Order.objects.create(
            customer=request.user if request.user.is_authenticated else None,
            shipping_address=shipping_address,
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
        "total": Cart.calculate_total(request.user if request.user.is_authenticated else session_key),
        "default_address": default_address
    })


def order_detail(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    return render(request, "order_detail.html", {"order": order})


def order_lookup(request):
    context = {}

    if request.method == "POST":
        order_id = request.POST.get("order_id")
        if order_id:
            try:
                order = Order.objects.get(order_id=order_id)
                return redirect('order_detail', order_id=order.order_id)
            except Order.DoesNotExist:
                context['error'] = "Pedido no encontrado."

    return render(request, "order_lookup.html", context)


def payment_complete_view(request):
    order_id = request.session.get('order_id_to_pay')

    if order_id:
        try:
            order = Order.objects.get(order_id=order_id)
            return render(request, "order_success.html", {"order": order})
        except Order.DoesNotExist:
            return redirect("view_cart")

    return redirect("view_cart")
