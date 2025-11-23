from django.db.models import Sum
from order.models import Cart

def cart_item_count(request):
    if request.user.is_authenticated:
        queryset = Cart.objects.filter(customer=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key

        queryset = Cart.objects.filter(session_key=session_key)

    total_items = queryset.aggregate(total=Sum("quantity"))["total"] or 0

    return {"cart_item_count": total_items}
