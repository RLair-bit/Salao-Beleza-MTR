from django.urls import path

from . import views

app_name = "servicos"

urlpatterns = [
    path("", views.listar, name="listar"),
    path("novo/", views.criar, name="criar"),
    path("<int:pk>/editar/", views.editar, name="editar"),
    path("<int:pk>/excluir/", views.excluir, name="excluir"),
]