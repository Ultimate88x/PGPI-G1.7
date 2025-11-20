from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def pagina_administrator(request):
    context = {}
    return render(request, 'administrator/administrator.html', context)