from datetime import time

from django.db import models
from django.utils.translation import gettext_lazy as _


class Configuracao(models.Model):
    IDIOMAS = [
        ("pt-pt", "Português (Portugal)"),
        ("es", "Español"),
        ("en", "English"),
        ("fr", "Français"),
    ]

    # Fusos agrupados por continente (rende <optgroup> no formulario)
    FUSOS = [
        ("Europa", [
            ("Europe/Lisbon", "Lisboa (Portugal)"),
            ("Europe/Madrid", "Madrid (Espanha)"),
            ("Europe/Paris", "Paris (França)"),
            ("Europe/London", "Londres (Reino Unido)"),
        ]),
        ("África", [
            ("Africa/Casablanca", "Casablanca (Marrocos)"),
            ("Africa/Lagos", "Lagos (Nigéria)"),
            ("Africa/Cairo", "Cairo (Egito)"),
            ("Africa/Johannesburg", "Joanesburgo (África do Sul)"),
        ]),
        ("América", [
            ("America/Sao_Paulo", "São Paulo (Brasil)"),
            ("America/New_York", "Nova Iorque (EUA)"),
            ("America/Mexico_City", "Cidade do México (México)"),
            ("America/Argentina/Buenos_Aires", "Buenos Aires (Argentina)"),
        ]),
        ("Ásia", [
            ("Asia/Dubai", "Dubai (Emirados)"),
            ("Asia/Kolkata", "Bombaim (Índia)"),
            ("Asia/Shanghai", "Xangai (China)"),
            ("Asia/Tokyo", "Tóquio (Japão)"),
        ]),
        ("Oceânia", [
            ("Australia/Sydney", "Sydney (Austrália)"),
            ("Pacific/Auckland", "Auckland (Nova Zelândia)"),
        ]),
    ]

    nome_salao = models.CharField(_("Nome do salão"), max_length=100, default="Salão de Beleza")
    telefone = models.CharField(_("Telefone"), max_length=30, blank=True)
    email = models.EmailField(_("Email"), blank=True)
    morada = models.CharField(_("Morada"), max_length=200, blank=True)
    hora_abertura = models.TimeField(_("Hora de abertura"), default=time(9, 0))
    hora_fecho = models.TimeField(_("Hora de fecho"), default=time(19, 0))
    idioma = models.CharField(_("Idioma"), max_length=5, choices=IDIOMAS, default="pt-pt")
    fuso_horario = models.CharField(_("Fuso horário"), max_length=40, choices=FUSOS, default="Europe/Lisbon")
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Configuração"
        verbose_name_plural = "Configurações"

    def __str__(self):
        return self.nome_salao

    def save(self, *args, **kwargs):
        self.pk = 1                      # garante um unico registo
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass                             # nao se apaga

    @classmethod
    def obter(cls):
        config, _ = cls.objects.get_or_create(pk=1)
        return config
