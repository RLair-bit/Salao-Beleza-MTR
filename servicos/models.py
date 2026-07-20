from django.db import models


class Servico(models.Model):
    nome = models.CharField("Serviço", max_length=120)
    preco = models.DecimalField("Preço (€)", max_digits=6, decimal_places=2)
    duracao_min = models.PositiveIntegerField("Duração (minutos)", default=30)
    ativo = models.BooleanField("Ativo", default=True)

    class Meta:
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"
        ordering = ["nome"]

    def __str__(self):
        return f"{self.nome} ({self.preco} €)"