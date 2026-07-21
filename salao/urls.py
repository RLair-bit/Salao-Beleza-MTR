from django.contrib import admin
from django.urls import include, path

from marcacoes.views import painel

urlpatterns = [
    path("admin/", admin.site.urls),
    path("marcacoes/", include("marcacoes.urls")),
    path("funcionarios/", include("funcionarios.urls")),
    path("contas/", include("django.contrib.auth.urls")),
    path("", painel, name="home"),
]