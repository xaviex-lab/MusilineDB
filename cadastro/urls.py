from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Raiz (index.html)
    path('contato/', views.contato, name='contato'),
    path('adicionar/', views.adicionar, name='adicionar'),
]
