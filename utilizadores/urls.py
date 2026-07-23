from django.urls import path

from . import views


app_name = "utilizadores"


urlpatterns = [
    path(
        "",
        views.lista,
        name="lista",
    ),
    path(
        "novo/",
        views.criar,
        name="criar",
    ),
    path(
        "minha-agenda/",
        views.minha_agenda,
        name="minha_agenda",
    ),
    path(
        "meu-perfil/",
        views.meu_perfil,
        name="meu_perfil",
    ),
    path(
        "<int:pk>/editar/",
        views.editar,
        name="editar",
    ),
    path(
        "<int:pk>/alterar-estado/",
        views.alterar_estado,
        name="alterar_estado",
    ),
]