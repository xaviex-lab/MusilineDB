# cadastro\urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contato/', views.contato, name='contato'),

    path('adicionar/', views.adicionar, name='adicionar'),

    path('faixa/<int:id>/', views.detalhe, name='detalhe'),

    path('faixa/<int:id>/editar/', views.editar, name='editar'),

    path('faixa/<int:id>/deletar/', views.deletar, name='deletar'),

    path('busca/', views.busca_ajax, name='busca_ajax'),

    path('registro/', views.registro, name='registro'),
]