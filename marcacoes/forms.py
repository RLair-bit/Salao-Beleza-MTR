from django import forms

from .models import Marcacao


class FuncionarioSelect(forms.Select):
    """
    Acrescenta informações da funcionária a cada opção
    do campo de seleção.
    """

    def create_option(
        self,
        name,
        value,
        label,
        selected,
        index,
        subindex=None,
        attrs=None,
    ):
        option = super().create_option(
            name,
            value,
            label,
            selected,
            index,
            subindex=subindex,
            attrs=attrs,
        )

        funcionario = getattr(
            value,
            "instance",
            None,
        )

        if funcionario is not None:
            foto_url = ""

            if funcionario.foto:
                try:
                    foto_url = funcionario.foto.url
                except ValueError:
                    foto_url = ""

            servicos = ", ".join(
                str(servico)
                for servico in funcionario.servicos.all()
            )

            option["attrs"].update(
                {
                    "data-foto": foto_url,
                    "data-funcao": funcionario.funcao or "",
                    "data-servicos": servicos,
                }
            )

        return option


class MarcacaoForm(forms.ModelForm):
    class Meta:
        model = Marcacao

        fields = [
            "cliente",
            "funcionario",
            "servico",
            "posto",
            "inicio",
            "estado",
            "notas",
        ]

        widgets = {
            "cliente": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "funcionario": FuncionarioSelect(
                attrs={
                    "class": "form-select",
                }
            ),
            "servico": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "posto": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "inicio": forms.HiddenInput(),
            "estado": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "notas": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["inicio"].input_formats = [
            "%Y-%m-%dT%H:%M",
        ]

        campo_funcionario = self.fields["funcionario"]

        campo_funcionario.queryset = (
            campo_funcionario.queryset
            .prefetch_related("servicos")
            .order_by("nome")
        )