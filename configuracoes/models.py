from datetime import time

from django.db import models


class Configuracao(models.Model):
    nome_salao = models.CharField("Nome do salão", max_length=100, default="Salão de Beleza")
    telefone = models.CharField("Telefone", max_length=30, blank=True)
    email = models.EmailField("Email", blank=True)
    morada = models.CharField("Morada", max_length=200, blank=True)
    hora_abertura = models.TimeField("Hora de abertura", default=time(9, 0))
    hora_fecho = models.TimeField("Hora de fecho", default=time(19, 0))
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