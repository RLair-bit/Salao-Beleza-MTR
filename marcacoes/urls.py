from django.urls import path

from . import views

app_name = "marcacoes"

urlpatterns = [
    path("", views.agenda, name="agenda"),
    path("nova/", views.criar, name="criar"),
]