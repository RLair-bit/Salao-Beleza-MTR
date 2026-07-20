from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models

from clientes.models import Cliente
from funcionarios.models import Funcionario
from servicos.models import Servico


class Posto(models.Model):
    numero = models.PositiveIntegerField("Número", unique=True)
    descricao = models.CharField("Descrição", max_length=80, blank=True)
    ativo = models.BooleanField("Ativo", default=True)

    class Meta:
        verbose_name = "Posto"
        verbose_name_plural = "Postos"
        ordering = ["numero"]

    def __str__(self):
        return f"Mesa {self.numero}"


class Marcacao(models.Model):
    ESTADOS = [
        ("marcada", "Marcada"),
        ("realizada", "Realizada"),
        ("cancelada", "Cancelada"),
        ("faltou", "Faltou"),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT,
                                related_name="marcacoes", verbose_name="Cliente")
    funcionario = models.ForeignKey(Funcionario, on_delete=models.PROTECT,
                                    related_name="marcacoes", verbose_name="Funcionário")
    servico = models.ForeignKey(Servico, on_delete=models.PROTECT,
                                related_name="marcacoes", verbose_name="Serviço")
    posto = models.ForeignKey(Posto, on_delete=models.PROTECT, null=True,
                              related_name="marcacoes", verbose_name="Mesa / Posto")
    inicio = models.DateTimeField("Data e hora")
    estado = models.CharField("Estado", max_length=10, choices=ESTADOS, default="marcada")
    notas = models.TextField("Notas", blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Marcação"
        verbose_name_plural = "Marcações"
        ordering = ["inicio"]

    def __str__(self):
        return f"{self.inicio:%d/%m/%Y %H:%M} - {self.cliente} com {self.funcionario}"

    @property
    def fim(self):
        return self.inicio + timedelta(minutes=self.servico.duracao_min)

    def clean(self):
        if not (self.inicio and self.servico_id and self.funcionario_id):
            return