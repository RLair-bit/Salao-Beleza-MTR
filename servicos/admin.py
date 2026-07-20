from django.contrib import admin

from .models import Servico


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ["nome", "preco", "duracao_min", "ativo"]
    list_filter = ["ativo"]
    search_fields = ["nome"]