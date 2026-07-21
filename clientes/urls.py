from django.urls import path

from . import views

app_name = "marcacoes"

urlpatterns = [
    path("", views.listar, name="cliente"),
    # path("nova/", views.criar, name="criar"),
    # path("<int:pk>/editar/", views.editar, name="editar"),
    # path("<int:pk>/estado/<str:estado>/", views.mudar_estado, name="mudar_estado"),
]