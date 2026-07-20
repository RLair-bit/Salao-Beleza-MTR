from django.contrib import admin

from .models import Marcacao, Posto


@admin.register(Marcacao)
class MarcacaoAdmin(admin.ModelAdmin):
    list_display = ["inicio", "cliente", "funcionario", "servico", "posto", "estado"]
    list_filter = ["estado", "funcionario"]
    date_hierarchy = "inicio"
    autocomplete_fields = ["cliente"]


@admin.register(Posto)
class PostoAdmin(admin.ModelAdmin):
    list_display = ["numero", "descricao", "ativo"]