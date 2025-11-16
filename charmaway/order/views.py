from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Cart, Order, OrderDetail, Address, Product


@login_required
def view_cart(request):
    items = Cart.objects.filter(customer=request.user)
    total = 0
    for item in items:
        item.subtotal = item.quantity * item.current_price
        total += item.subtotal

    return render(request, "cart.html", {
        "items": items,
        "total": total
    })


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    try:
        quantity = int(request.POST.get("quantity", 1))
        if quantity < 1:
            quantity = 1
    except (ValueError, TypeError):
        quantity = 1

    cart_item, created = Cart.objects.get_or_create(
        customer=request.user,
        product=product,
        defaults={"current_price": product.price, "quantity": quantity}
    )

    if not created:
        cart_item.quantity += quantity

    cart_item.current_price = product.price
    cart_item.save()

    return redirect("view_cart")


@login_required
def decrease_from_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart_item = get_object_or_404(Cart, customer=request.user, product=product)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect("view_cart")


@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart_item = get_object_or_404(Cart, customer=request.user, product=product)
    cart_item.delete()
    return redirect("view_cart")


@login_required
def clear_cart(request):
    Cart.clear_cart(request.user)
    return redirect("view_cart")


@login_required
def checkout(request):
    cart_items = Cart.objects.filter(customer=request.user)
    if not cart_items.exists():
        return redirect("view_cart")

    default_address = Address.objects.filter(user=request.user, is_default=True).first()

    if request.method == "POST":
        if default_address:
            shipping_address = default_address
        else:
            shipping_address = Address.objects.create(
                user=request.user,
                street=request.POST.get('street'),
                number=request.POST.get('number'),
                floor=request.POST.get('floor'),
                postal_code=request.POST.get('postal_code'),
                city=request.POST.get('city'),
                state=request.POST.get('state'),
                country=request.POST.get('country'),
            )


        order = Order.objects.create(
            customer=request.user,
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
                subtotal=item.current_price * item.quantity
            )

        order.calculate_total()
        order.save()
        request.session['order_id_to_pay'] = order.order_id 
        if order.payment_method == 'credit_card':
            return redirect('payment:checkout')
        
        elif order.payment_method == 'paypal':
            return redirect('paypal:process_payment') # Ejemplo
        
        else:
            return redirect('payment:checkout')

    return render(request, "checkout.html", {
        "cart_items": cart_items,
        "total": Cart.calculate_total(request.user),
        "default_address": default_address
    })


@login_required
def order_detail(request, order_id):
    order = Order.objects.get(order_id=order_id)
    return render(request, "order_detail.html", {"order": order})


def order_lookup(request):
    context = {}

    if request.method == "POST":
        order_id = request.POST.get("order_id")
        if order_id:
            try:
                order = Order.objects.get(order_id=order_id, customer=request.user)
                return redirect('order_detail', order_id=order.order_id)
            except Order.DoesNotExist:
                context['error'] = "Pedido no encontrado."

    return render(request, "order_lookup.html", context)


@login_required
def payment_complete_view(request):
    """
    Página genérica de éxito de pago.
    Recupera el pedido de la sesión y muestra la plantilla order_success.
    """
    order_id = request.session.get('order_id_to_pay')
    
    if order_id:
        try:

            order = Order.objects.get(order_id=order_id, customer=request.user)
            return render(request, "order_success.html", {"order": order})
        
        except Order.DoesNotExist:
            return redirect("view_cart")
        
    return redirect("view_cart")