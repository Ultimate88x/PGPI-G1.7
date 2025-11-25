from django.db.models import Sum
from order.models import Cart
from catalog.models import Department, Category, Brand

def cart_item_count(request):
    session_key = request.session.session_key

    if request.user.is_authenticated:
        queryset = Cart.objects.filter(customer=request.user)
    elif session_key is None:
        return {"cart_item_count": 0}
    else:
        queryset = Cart.objects.filter(session_key=session_key)

    total_items = queryset.aggregate(total=Sum("quantity"))["total"] or 0

    return {"cart_item_count": total_items}

def search_filters(request):
    """Provide departments and brands for search filters in all templates"""
    # Include all departments (including Services) in the search dropdown
    return {
        "all_departments": Department.objects.all().order_by('order_position', 'name'),
        "all_brands": Brand.objects.all().order_by('name')
    }
