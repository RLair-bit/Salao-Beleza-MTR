from django.urls import path

from . import views

app_name = "clientes"

urlpatterns = [
    path("", views.listar, name="lista"),
    # path("nova/", views.criar, name="criar"),
    # path("<int:pk>/editar/", views.editar, name="editar"),
    # path("<int:pk>/estado/<str:estado>/", views.mudar_estado, name="mudar_estado"),
]