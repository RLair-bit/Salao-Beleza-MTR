from django.contrib import admin

from .models import Marcacao


@admin.register(Marcacao)
class MarcacaoAdmin(admin.ModelAdmin):
    list_display = ["inicio", "cliente", "funcionario", "servico", "estado"]
    list_filter = ["estado", "funcionario"]
    date_hierarchy = "inicio"
    autocomplete_fields = ["cliente"]