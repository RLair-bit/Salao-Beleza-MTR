from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from clientes.models import Cliente
from funcionarios.models import Funcionario
from servicos.models import Servico


class Posto(models.Model):
    numero = models.PositiveIntegerField(
        "Número",
        unique=True,
    )
    descricao = models.CharField(
        "Descrição",
        max_length=80,
        blank=True,
    )
    ativo = models.BooleanField(
        "Ativo",
        default=True,
    )

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

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name="marcacoes",
        verbose_name="Cliente",
    )

    funcionario = models.ForeignKey(
        Funcionario,
        on_delete=models.PROTECT,
        related_name="marcacoes",
        verbose_name="Funcionário",
    )

    servico = models.ForeignKey(
        Servico,
        on_delete=models.PROTECT,
        related_name="marcacoes",
        verbose_name="Serviço",
    )

    posto = models.ForeignKey(
        Posto,
        on_delete=models.PROTECT,
        null=True,
        related_name="marcacoes",
        verbose_name="Mesa / Posto",
    )

    inicio = models.DateTimeField(
        "Data e hora",
    )

    estado = models.CharField(
        "Estado",
        max_length=10,
        choices=ESTADOS,
        default="marcada",
    )

    notas = models.TextField(
        "Notas",
        blank=True,
    )

    criado_em = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Marcação"
        verbose_name_plural = "Marcações"
        ordering = ["inicio"]

    def __str__(self):
        inicio_local = timezone.localtime(self.inicio)

        return (
            f"{inicio_local:%d/%m/%Y %H:%M} - "
            f"{self.cliente} com {self.funcionario}"
        )

    @property
    def fim(self):
        return self.inicio + timedelta(
            minutes=self.servico.duracao_min
        )

    @property
    def a_decorrer(self):
        agora = timezone.now()

        return (
            self.estado == "marcada"
            and self.inicio <= agora < self.fim
        )

    @property
    def em_atraso(self):
        return (
            self.estado == "marcada"
            and self.fim <= timezone.now()
        )

    def clean(self):
        if not (
            self.inicio
            and self.servico_id
            and self.funcionario_id
        ):
            return

        if self.estado == "cancelada":
            return

        margem = timedelta(hours=12)

        possiveis = (
            Marcacao.objects
            .filter(
                inicio__gte=self.inicio - margem,
                inicio__lte=self.inicio + margem,
            )
            .exclude(pk=self.pk)
            .exclude(estado="cancelada")
            .select_related(
                "servico",
                "funcionario",
                "posto",
            )
        )

        for marcacao_existente in possiveis:
            existe_sobreposicao = (
                self.inicio < marcacao_existente.fim
                and marcacao_existente.inicio < self.fim
            )

            if not existe_sobreposicao:
                continue

            inicio_local = timezone.localtime(
                marcacao_existente.inicio
            )

            fim_local = timezone.localtime(
                marcacao_existente.fim
            )

            if (
                marcacao_existente.funcionario_id
                == self.funcionario_id
            ):
                raise ValidationError(
                    f"{self.funcionario} já tem uma marcação "
                    f"das {inicio_local:%H:%M} "
                    f"às {fim_local:%H:%M}."
                )

            if (
                self.posto_id
                and marcacao_existente.posto_id
                == self.posto_id
            ):
                raise ValidationError(
                    f"A {marcacao_existente.posto} já está "
                    f"ocupada das {inicio_local:%H:%M} "
                    f"às {fim_local:%H:%M}."
                )

    def save(self, *args, **kwargs):
        self.full_clean()

        return super().save(*args, **kwargs)