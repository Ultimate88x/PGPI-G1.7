from django.db.models import Sum
from order.models import Cart

def cart_item_count(request):
    if request.user.is_authenticated:
        total_items = Cart.objects.filter(customer=request.user).aggregate(
            total_quantity=Sum('quantity')
        )['total_quantity'] or 0
    else:
        total_items = 0
    return {'cart_item_count': total_items}
