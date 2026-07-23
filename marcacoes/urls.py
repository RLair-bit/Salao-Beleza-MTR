from django.urls import path

from . import views


app_name = "marcacoes"


urlpatterns = [
    path(
        "",
        views.agenda,
        name="agenda",
    ),
    path(
        "nova/",
        views.criar,
        name="criar",
    ),
    path(
        "pendentes/",
        views.pendentes,
        name="pendentes",
    ),
    path(
        "horarios-disponiveis/",
        views.horarios_disponiveis,
        name="horarios_disponiveis",
    ),
    path(
        "<int:pk>/editar/",
        views.editar,
        name="editar",
    ),
    path(
        "<int:pk>/estado/<str:estado>/",
        views.mudar_estado,
        name="mudar_estado",
    ),
]