from django.db import models

from servicos.models import Servico


class Funcionario(models.Model):
    nome = models.CharField("Nome", max_length=120)
    telefone = models.CharField("Telefone", max_length=20, blank=True)
    funcao = models.CharField("Função", max_length=80, blank=True)
    servicos = models.ManyToManyField(Servico, verbose_name="Serviços que presta", blank=True)
    ativo = models.BooleanField("Ativo", default=True)

    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"
        ordering = ["nome"]

    def __str__(self):
        return self.nome