from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from clientes.models import Cliente
from funcionarios.models import Funcionario
from servicos.models import Servico


class Posto(models.Model):
    numero = models.PositiveIntegerField(_("Número"), unique=True)
    descricao = models.CharField(_("Descrição"), max_length=80, blank=True)
    ativo = models.BooleanField(_("Ativo"), default=True)

    class Meta:
        verbose_name = _("Posto")
        verbose_name_plural = _("Postos")
        ordering = ["numero"]

    def __str__(self):
        return f"Mesa {self.numero}"


class Marcacao(models.Model):
    ESTADOS = [
        ("marcada", _("Marcada")),
        ("realizada", _("Realizada")),
        ("cancelada", _("Cancelada")),
        ("faltou", _("Faltou")),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT,
                                related_name="marcacoes", verbose_name=_("Cliente"))
    funcionario = models.ForeignKey(Funcionario, on_delete=models.PROTECT,
                                    related_name="marcacoes", verbose_name=_("Funcionário"))
    servico = models.ForeignKey(Servico, on_delete=models.PROTECT,
                                related_name="marcacoes", verbose_name=_("Serviço"))
    posto = models.ForeignKey(Posto, on_delete=models.PROTECT, null=True,
                              related_name="marcacoes", verbose_name=_("Mesa / Posto"))
    inicio = models.DateTimeField(_("Data e hora"))
    estado = models.CharField(_("Estado"), max_length=10, choices=ESTADOS, default="marcada")
    notas = models.TextField(_("Notas"), blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Marcação")
        verbose_name_plural = _("Marcações")
        ordering = ["inicio"]

    def __str__(self):
        return f"{self.inicio:%d/%m/%Y %H:%M} - {self.cliente} com {self.funcionario}"

    @property
    def fim(self):
        return self.inicio + timedelta(minutes=self.servico.duracao_min)

    @property
    def a_decorrer(self):
        agora = timezone.now()
        return self.estado == "marcada" and self.inicio <= agora < self.fim

    @property
    def em_atraso(self):
        return self.estado == "marcada" and self.fim <= timezone.now()

    def clean(self):
        if not (self.inicio and self.servico_id and self.funcionario_id):
            return
        if self.estado == "cancelada":
            return

        margem = timedelta(hours=12)
        possiveis = (
            Marcacao.objects
            .filter(inicio__gte=self.inicio - margem, inicio__lte=self.inicio + margem)
            .exclude(pk=self.pk)
            .exclude(estado="cancelada")
            .select_related("servico", "funcionario", "posto")
        )
        for m in possiveis:
            if not (self.inicio < m.fim and m.inicio < self.fim):
                continue
            if m.funcionario_id == self.funcionario_id:
                raise ValidationError(
                    _("%(funcionario)s já tem uma marcação das "
                      "%(inicio)s às %(fim)s.") % {
                        "funcionario": self.funcionario,
                        "inicio": f"{m.inicio:%H:%M}",
                        "fim": f"{m.fim:%H:%M}",
                    }
                )
            if self.posto_id and m.posto_id == self.posto_id:
                raise ValidationError(
                    _("A %(posto)s já está ocupada das "
                      "%(inicio)s às %(fim)s.") % {
                        "posto": m.posto,
                        "inicio": f"{m.inicio:%H:%M}",
                        "fim": f"{m.fim:%H:%M}",
                    }
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)