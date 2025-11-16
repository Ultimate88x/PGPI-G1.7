from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Cart, Order, OrderDetail, Address, Product


@login_required
def view_cart(request):
    """Mostrar el carrito del usuario actual."""
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
    """Añadir un producto al carrito (o sumar cantidad si ya existe)."""
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
    """Restar una unidad del producto del carrito."""
    product = get_object_or_404(Product, pk=product_id)
    cart_item = get_object_or_404(Cart, customer=request.user, product=product)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        # Si queda 1 y se resta, se elimina
        cart_item.delete()

    return redirect("view_cart")


@login_required
def remove_from_cart(request, product_id):
    """Eliminar completamente un producto del carrito."""
    product = get_object_or_404(Product, pk=product_id)
    cart_item = get_object_or_404(Cart, customer=request.user, product=product)
    cart_item.delete()
    return redirect("view_cart")


@login_required
def clear_cart(request):
    """Vaciar totalmente el carrito."""
    Cart.clear_cart(request.user)
    return redirect("view_cart")


@login_required
def checkout(request):
    """Vista para procesar la creación de la orden."""
    cart_items = Cart.objects.filter(customer=request.user)
    if not cart_items.exists():
        # Si no hay items, redirige al carrito
        return redirect("view_cart")

    default_address = Address.objects.filter(user=request.user, is_default=True).first()

    if request.method == "POST":
        # Obtener o crear dirección
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

        # Crear la orden
        order = Order.objects.create(
            customer=request.user,
            shipping_address=shipping_address,
            payment_method=request.POST.get('payment_method'),
            notes=request.POST.get('notes', '')
        )

        # Copiar items del carrito al detalle de la orden
        for item in cart_items:
            OrderDetail.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                unit_price=item.current_price,
                subtotal=item.current_price * item.quantity
            )

        # Calcular totales
        order.calculate_total()

        # Vaciar carrito
        Cart.clear_cart(request.user)

        # Redirigir a una página de éxito o detalle de orden
        return redirect("order_success", order_id=order.order_id)

    return render(request, "checkout.html", {
        "cart_items": cart_items,
        "total": Cart.calculate_total(request.user),
        "default_address": default_address
    })


@login_required
def order_success(request, order_id):
    """Muestra un mensaje de confirmación tras crear la orden."""
    order = Order.objects.get(order_id=order_id)
    return render(request, "order_success.html", {"order": order})


@login_required
def order_detail(request, order_id):
    order = Order.objects.get(order_id=order_id)
    return render(request, "order_detail.html", {"order": order})


def order_lookup(request):
    """
    Permite al usuario introducir un ID de pedido y ver su detalle.
    """
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