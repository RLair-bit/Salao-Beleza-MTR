from django import forms

from .models import (
    AusenciaFuncionario,
    Funcionario,
    HorarioTrabalho,
)


class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario

        fields = [
            "foto",
            "nome",
            "telefone",
            "funcao",
            "servicos",
            "ativo",
        ]

        widgets = {
            "foto": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/jpeg,image/png,image/webp",
                }
            ),
            "nome": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nome completo do funcionário",
                }
            ),
            "telefone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex.: 912 345 678",
                }
            ),
            "funcao": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex.: Cabeleireira",
                }
            ),
            "servicos": forms.CheckboxSelectMultiple(),
            "ativo": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }


class HorarioTrabalhoCriarForm(forms.Form):
    dias_semana = forms.MultipleChoiceField(
        label="Dias da semana",
        choices=HorarioTrabalho.DIAS_SEMANA,
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "class": "form-check-input",
            }
        ),
        help_text=(
            "De segunda-feira a sexta-feira ficam "
            "selecionados automaticamente."
        ),
    )

    hora_inicio = forms.TimeField(
        label="Hora de entrada",
        widget=forms.TimeInput(
            attrs={
                "class": "form-control",
                "type": "time",
            },
            format="%H:%M",
        ),
        input_formats=[
            "%H:%M",
            "%H:%M:%S",
        ],
    )

    hora_fim = forms.TimeField(
        label="Hora de saída",
        widget=forms.TimeInput(
            attrs={
                "class": "form-control",
                "type": "time",
            },
            format="%H:%M",
        ),
        input_formats=[
            "%H:%M",
            "%H:%M:%S",
        ],
    )

    intervalo_inicio = forms.TimeField(
        label="Início do intervalo",
        required=False,
        widget=forms.TimeInput(
            attrs={
                "class": "form-control",
                "type": "time",
            },
            format="%H:%M",
        ),
        input_formats=[
            "%H:%M",
            "%H:%M:%S",
        ],
    )

    intervalo_fim = forms.TimeField(
        label="Fim do intervalo",
        required=False,
        widget=forms.TimeInput(
            attrs={
                "class": "form-control",
                "type": "time",
            },
            format="%H:%M",
        ),
        input_formats=[
            "%H:%M",
            "%H:%M:%S",
        ],
    )

    ativo = forms.BooleanField(
        label="Trabalha nestes dias",
        required=False,
        initial=True,
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
            }
        ),
    )

    def __init__(
        self,
        *args,
        funcionario=None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.funcionario = funcionario

        dias_padrao = [
            HorarioTrabalho.SEGUNDA,
            HorarioTrabalho.TERCA,
            HorarioTrabalho.QUARTA,
            HorarioTrabalho.QUINTA,
            HorarioTrabalho.SEXTA,
        ]

        if funcionario:
            dias_existentes = set(
                funcionario.horarios.values_list(
                    "dia_semana",
                    flat=True,
                )
            )

            dias_padrao = [
                dia
                for dia in dias_padrao
                if dia not in dias_existentes
            ]

        if not self.is_bound:
            self.fields["dias_semana"].initial = dias_padrao

    def clean_dias_semana(self):
        dias_semana = self.cleaned_data["dias_semana"]

        if not dias_semana:
            raise forms.ValidationError(
                "Selecione pelo menos um dia da semana."
            )

        if self.funcionario:
            dias_existentes = set(
                self.funcionario.horarios.values_list(
                    "dia_semana",
                    flat=True,
                )
            )

            dias_repetidos = [
                int(dia)
                for dia in dias_semana
                if int(dia) in dias_existentes
            ]

            if dias_repetidos:
                nomes_dias = dict(
                    HorarioTrabalho.DIAS_SEMANA
                )

                dias_formatados = ", ".join(
                    nomes_dias[dia]
                    for dia in dias_repetidos
                )

                raise forms.ValidationError(
                    "Já existe horário para: "
                    f"{dias_formatados}. "
                    "Edite esses horários na lista."
                )

        return dias_semana

    def clean(self):
        dados = super().clean()

        hora_inicio = dados.get("hora_inicio")
        hora_fim = dados.get("hora_fim")
        intervalo_inicio = dados.get(
            "intervalo_inicio"
        )
        intervalo_fim = dados.get(
            "intervalo_fim"
        )

        if (
            hora_inicio
            and hora_fim
            and hora_fim <= hora_inicio
        ):
            self.add_error(
                "hora_fim",
                (
                    "A hora de saída deve ser posterior "
                    "à hora de entrada."
                ),
            )

        tem_inicio_intervalo = (
            intervalo_inicio is not None
        )

        tem_fim_intervalo = (
            intervalo_fim is not None
        )

        if tem_inicio_intervalo != tem_fim_intervalo:
            mensagem = (
                "Preencha o início e o fim do intervalo."
            )

            self.add_error(
                "intervalo_inicio",
                mensagem,
            )

            self.add_error(
                "intervalo_fim",
                mensagem,
            )

        if intervalo_inicio and intervalo_fim:
            if intervalo_fim <= intervalo_inicio:
                self.add_error(
                    "intervalo_fim",
                    (
                        "O fim do intervalo deve ser "
                        "posterior ao início."
                    ),
                )

            if (
                hora_inicio
                and intervalo_inicio <= hora_inicio
            ):
                self.add_error(
                    "intervalo_inicio",
                    (
                        "O intervalo deve começar depois "
                        "da hora de entrada."
                    ),
                )

            if (
                hora_fim
                and intervalo_fim >= hora_fim
            ):
                self.add_error(
                    "intervalo_fim",
                    (
                        "O intervalo deve terminar antes "
                        "da hora de saída."
                    ),
                )

        return dados


class HorarioTrabalhoForm(forms.ModelForm):
    class Meta:
        model = HorarioTrabalho

        fields = [
            "dia_semana",
            "hora_inicio",
            "hora_fim",
            "intervalo_inicio",
            "intervalo_fim",
            "ativo",
        ]

        widgets = {
            "dia_semana": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "hora_inicio": forms.TimeInput(
                attrs={
                    "class": "form-control",
                    "type": "time",
                },
                format="%H:%M",
            ),
            "hora_fim": forms.TimeInput(
                attrs={
                    "class": "form-control",
                    "type": "time",
                },
                format="%H:%M",
            ),
            "intervalo_inicio": forms.TimeInput(
                attrs={
                    "class": "form-control",
                    "type": "time",
                },
                format="%H:%M",
            ),
            "intervalo_fim": forms.TimeInput(
                attrs={
                    "class": "form-control",
                    "type": "time",
                },
                format="%H:%M",
            ),
            "ativo": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

        help_texts = {
            "intervalo_inicio": (
                "Campo opcional. Preencha apenas "
                "se existir intervalo."
            ),
            "intervalo_fim": (
                "Campo opcional. Preencha apenas "
                "se existir intervalo."
            ),
            "ativo": (
                "Desmarque para suspender "
                "temporariamente este horário."
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["hora_inicio"].input_formats = [
            "%H:%M",
            "%H:%M:%S",
        ]

        self.fields["hora_fim"].input_formats = [
            "%H:%M",
            "%H:%M:%S",
        ]

        self.fields[
            "intervalo_inicio"
        ].input_formats = [
            "%H:%M",
            "%H:%M:%S",
        ]

        self.fields[
            "intervalo_fim"
        ].input_formats = [
            "%H:%M",
            "%H:%M:%S",
        ]


class AusenciaFuncionarioForm(forms.ModelForm):
    class Meta:
        model = AusenciaFuncionario

        fields = [
            "tipo",
            "data_inicio",
            "data_fim",
            "dia_inteiro",
            "hora_inicio",
            "hora_fim",
            "motivo",
        ]

        widgets = {
            "tipo": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "data_inicio": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                },
                format="%Y-%m-%d",
            ),
            "data_fim": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                },
                format="%Y-%m-%d",
            ),
            "dia_inteiro": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "hora_inicio": forms.TimeInput(
                attrs={
                    "class": "form-control",
                    "type": "time",
                },
                format="%H:%M",
            ),
            "hora_fim": forms.TimeInput(
                attrs={
                    "class": "form-control",
                    "type": "time",
                },
                format="%H:%M",
            ),
            "motivo": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": (
                        "Indique uma observação, "
                        "caso seja necessário."
                    ),
                }
            ),
        }

        help_texts = {
            "dia_inteiro": (
                "Quando esta opção estiver marcada, "
                "não é necessário indicar as horas."
            ),
            "hora_inicio": (
                "Preencha apenas para uma "
                "ausência parcial."
            ),
            "hora_fim": (
                "Preencha apenas para uma "
                "ausência parcial."
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["data_inicio"].input_formats = [
            "%Y-%m-%d",
        ]

        self.fields["data_fim"].input_formats = [
            "%Y-%m-%d",
        ]

        self.fields["hora_inicio"].input_formats = [
            "%H:%M",
            "%H:%M:%S",
        ]

        self.fields["hora_fim"].input_formats = [
            "%H:%M",
            "%H:%M:%S",
        ]