from django.urls import path

from . import views


app_name = "funcionarios"


urlpatterns = [
    # Funcionários
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

    # Horários de trabalho
    path(
        "<int:funcionario_pk>/horarios/",
        views.horarios_lista,
        name="horarios_lista",
    ),
    path(
        "<int:funcionario_pk>/horarios/novo/",
        views.horario_criar,
        name="horario_criar",
    ),
    path(
        "horarios/<int:pk>/editar/",
        views.horario_editar,
        name="horario_editar",
    ),
    path(
        "horarios/<int:pk>/eliminar/",
        views.horario_eliminar,
        name="horario_eliminar",
    ),

    # Ausências, folgas e férias
    path(
        "<int:funcionario_pk>/ausencias/",
        views.ausencias_lista,
        name="ausencias_lista",
    ),
    path(
        "<int:funcionario_pk>/ausencias/nova/",
        views.ausencia_criar,
        name="ausencia_criar",
    ),
    path(
        "ausencias/<int:pk>/editar/",
        views.ausencia_editar,
        name="ausencia_editar",
    ),
    path(
        "ausencias/<int:pk>/eliminar/",
        views.ausencia_eliminar,
        name="ausencia_eliminar",
    ),

    # Detalhes, edição e eliminação
    path(
        "<int:pk>/",
        views.detalhe,
        name="detalhe",
    ),
    path(
        "<int:pk>/editar/",
        views.editar,
        name="editar",
    ),
    path(
        "<int:pk>/eliminar/",
        views.eliminar,
        name="eliminar",
    ),
]