from order.models import Cart

def cart_item_count(request):
    session_key = request.session.session_key

    if request.user.is_authenticated:
        count = Cart.objects.filter(customer=request.user).count()
        return {"cart_item_count": count}

    if session_key is None:
        return {"cart_item_count": 0}

    count = Cart.objects.filter(session_key=session_key).count()
    return {"cart_item_count": count}
