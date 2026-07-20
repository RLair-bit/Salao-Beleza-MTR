
from django.db import models


class Cliente(models.Model):
    nome = models.CharField("Nome", max_length=120)
    telefone = models.CharField("Telefone", max_length=20)
    email = models.EmailField("Email", blank=True)
    observacoes = models.TextField("Observações", blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["nome"]

    def __str__(self):
        return self.nome