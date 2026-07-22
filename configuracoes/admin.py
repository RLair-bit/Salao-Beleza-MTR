from django.contrib import admin

from .models import Configuracao


@admin.register(Configuracao)
class ConfiguracaoAdmin(admin.ModelAdmin):
    list_display = ["nome_salao", "telefone", "email", "atualizado_em"]
