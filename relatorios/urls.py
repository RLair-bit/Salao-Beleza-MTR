from django.urls import path

from . import views

app_name = "relatorios"

urlpatterns = [
    path("servicos/", views.relatorio_servicos, name="servicos", ),
]