from django.urls import path
from . import views

app_name = 'administrator'

urlpatterns = [
    path('', views.pagina_administrator, name='administrator')
]