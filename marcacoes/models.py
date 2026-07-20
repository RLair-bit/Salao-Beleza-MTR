from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models

from clientes.models import Cliente
from funcionarios.models import Funcionario
from servicos.models import Servico


class Marcacao(models.Model):
    ESTADOS = [
        ("marcada", "Marcada"),
        ("realizada", "Realizada"),
        ("cancelada", "Cancelada"),
        ("faltou", "Faltou"),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name="marcacoes")
    funcionario = models.ForeignKey(Funcionario, on_delete=models.PROTECT, related_name="marcacoes")
    servico = models.ForeignKey(Servico, on_delete=models.PROTECT, related_name="marcacoes")
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
        if self.estado == "cancelada":
            return

        margem = timedelta(hours=12)
        possiveis = (
            Marcacao.objects
            .filter(funcionario_id=self.funcionario_id,
                    inicio__gte=self.inicio - margem,
                    inicio__lte=self.inicio + margem)
            .exclude(pk=self.pk)
            .exclude(estado="cancelada")
        )
        for m in possiveis:
            if self.inicio < m.fim and m.inicio < self.fim:
                raise ValidationError(
                    f"{self.funcionario} já tem uma marcação das "
                    f"{m.inicio:%H:%M} às {m.fim:%H:%M}."
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)