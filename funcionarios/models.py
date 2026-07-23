from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from servicos.models import Servico


class Funcionario(models.Model):
    utilizador = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="funcionario",
        verbose_name="Utilizador associado",
    )

    foto = models.ImageField(
        "Fotografia",
        upload_to="funcionarios/",
        null=True,
        blank=True,
    )

    nome = models.CharField(
        "Nome",
        max_length=120,
    )

    telefone = models.CharField(
        "Telefone",
        max_length=20,
        blank=True,
    )

    funcao = models.CharField(
        "Função",
        max_length=80,
        blank=True,
    )

    servicos = models.ManyToManyField(
        Servico,
        verbose_name="Serviços que presta",
        blank=True,
    )

    ativo = models.BooleanField(
        "Ativo",
        default=True,
    )

    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class HorarioTrabalho(models.Model):
    SEGUNDA = 0
    TERCA = 1
    QUARTA = 2
    QUINTA = 3
    SEXTA = 4
    SABADO = 5
    DOMINGO = 6

    DIAS_SEMANA = [
        (SEGUNDA, "Segunda-feira"),
        (TERCA, "Terça-feira"),
        (QUARTA, "Quarta-feira"),
        (QUINTA, "Quinta-feira"),
        (SEXTA, "Sexta-feira"),
        (SABADO, "Sábado"),
        (DOMINGO, "Domingo"),
    ]

    funcionario = models.ForeignKey(
        Funcionario,
        on_delete=models.CASCADE,
        related_name="horarios",
        verbose_name="Funcionário",
    )

    dia_semana = models.PositiveSmallIntegerField(
        "Dia da semana",
        choices=DIAS_SEMANA,
    )

    hora_inicio = models.TimeField(
        "Hora de entrada",
    )

    hora_fim = models.TimeField(
        "Hora de saída",
    )

    intervalo_inicio = models.TimeField(
        "Início do intervalo",
        null=True,
        blank=True,
    )

    intervalo_fim = models.TimeField(
        "Fim do intervalo",
        null=True,
        blank=True,
    )

    ativo = models.BooleanField(
        "Trabalha neste dia",
        default=True,
    )

    class Meta:
        verbose_name = "Horário de trabalho"
        verbose_name_plural = "Horários de trabalho"
        ordering = [
            "funcionario__nome",
            "dia_semana",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "funcionario",
                    "dia_semana",
                ],
                name="horario_unico_por_funcionario_dia",
            ),
        ]

    def clean(self):
        erros = {}

        if self.hora_inicio and self.hora_fim:
            if self.hora_fim <= self.hora_inicio:
                erros["hora_fim"] = (
                    "A hora de saída deve ser posterior "
                    "à hora de entrada."
                )

        tem_inicio_intervalo = self.intervalo_inicio is not None
        tem_fim_intervalo = self.intervalo_fim is not None

        if tem_inicio_intervalo != tem_fim_intervalo:
            erros["intervalo_inicio"] = (
                "Preencha o início e o fim do intervalo."
            )
            erros["intervalo_fim"] = (
                "Preencha o início e o fim do intervalo."
            )

        if (
            self.intervalo_inicio
            and self.intervalo_fim
        ):
            if self.intervalo_fim <= self.intervalo_inicio:
                erros["intervalo_fim"] = (
                    "O fim do intervalo deve ser posterior "
                    "ao início do intervalo."
                )

            if (
                self.hora_inicio
                and self.intervalo_inicio <= self.hora_inicio
            ):
                erros["intervalo_inicio"] = (
                    "O intervalo deve começar depois "
                    "da hora de entrada."
                )

            if (
                self.hora_fim
                and self.intervalo_fim >= self.hora_fim
            ):
                erros["intervalo_fim"] = (
                    "O intervalo deve terminar antes "
                    "da hora de saída."
                )

        if erros:
            raise ValidationError(erros)

    def __str__(self):
        return (
            f"{self.funcionario.nome} - "
            f"{self.get_dia_semana_display()}"
        )


class AusenciaFuncionario(models.Model):
    FOLGA = "folga"
    FERIAS = "ferias"
    DOENCA = "doenca"
    OUTRO = "outro"

    TIPOS_AUSENCIA = [
        (FOLGA, "Folga"),
        (FERIAS, "Férias"),
        (DOENCA, "Doença"),
        (OUTRO, "Outro"),
    ]

    funcionario = models.ForeignKey(
        Funcionario,
        on_delete=models.CASCADE,
        related_name="ausencias",
        verbose_name="Funcionário",
    )

    tipo = models.CharField(
        "Tipo de ausência",
        max_length=20,
        choices=TIPOS_AUSENCIA,
        default=FOLGA,
    )

    data_inicio = models.DateField(
        "Data de início",
    )

    data_fim = models.DateField(
        "Data de fim",
    )

    dia_inteiro = models.BooleanField(
        "Dia inteiro",
        default=True,
    )

    hora_inicio = models.TimeField(
        "Hora de início",
        null=True,
        blank=True,
    )

    hora_fim = models.TimeField(
        "Hora de fim",
        null=True,
        blank=True,
    )

    motivo = models.CharField(
        "Motivo ou observação",
        max_length=200,
        blank=True,
    )

    class Meta:
        verbose_name = "Ausência do funcionário"
        verbose_name_plural = "Ausências dos funcionários"
        ordering = [
            "-data_inicio",
            "funcionario__nome",
        ]

    def clean(self):
        erros = {}

        if (
            self.data_inicio
            and self.data_fim
            and self.data_fim < self.data_inicio
        ):
            erros["data_fim"] = (
                "A data de fim não pode ser anterior "
                "à data de início."
            )

        if not self.dia_inteiro:
            if not self.hora_inicio:
                erros["hora_inicio"] = (
                    "Indique a hora de início da ausência."
                )

            if not self.hora_fim:
                erros["hora_fim"] = (
                    "Indique a hora de fim da ausência."
                )

            if (
                self.hora_inicio
                and self.hora_fim
                and self.hora_fim <= self.hora_inicio
            ):
                erros["hora_fim"] = (
                    "A hora de fim deve ser posterior "
                    "à hora de início."
                )

            if (
                self.data_inicio
                and self.data_fim
                and self.data_inicio != self.data_fim
            ):
                erros["data_fim"] = (
                    "Uma ausência parcial deve ocorrer "
                    "num único dia."
                )

        if erros:
            raise ValidationError(erros)

    def save(self, *args, **kwargs):
        if self.dia_inteiro:
            self.hora_inicio = None
            self.hora_fim = None

        self.full_clean()

        return super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.funcionario.nome} - "
            f"{self.get_tipo_display()} - "
            f"{self.data_inicio}"
        )