from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from utilizadores.inicio import inicio


urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),
    path(
        "clientes/",
        include("clientes.urls"),
    ),
    path(
        "marcacoes/",
        include("marcacoes.urls"),
    ),
    path(
        "funcionarios/",
        include("funcionarios.urls"),
    ),
    path(
        "utilizadores/",
        include("utilizadores.urls"),
    ),
    path(
        "contas/",
        include("django.contrib.auth.urls"),
    ),
    path(
        "mapa/",
        include("mapa.urls"),
    ),
    path(
        "servicos/",
        include("servicos.urls"),
    ),
    path(
        "configuracoes/",
        include("configuracoes.urls"),
    ),
    path(
        "relatorios/",
        include("relatorios.urls"),
    ),
    path(
        "",
        inicio,
        name="home",
    ),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )