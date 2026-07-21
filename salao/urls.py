from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("marcacoes/", include("marcacoes.urls")),
    path("funcionarios/", include("funcionarios.urls")),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
]