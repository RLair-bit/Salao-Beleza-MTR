from django import forms
from django.utils.translation import gettext as _

from marcacoes.models import Marcacao

class RelatorioServicoForm(forms.Form):

    data_inicial = forms.DateField(
        required=True,
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
            }
        )
    )

    data_final = forms.DateField(
        required=True,
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
            }
        )
    )

    estados = forms.MultipleChoiceField(
        choices=Marcacao.ESTADOS,
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    def clean(self):
        cleaned_data = super().clean()

        data_inicial = cleaned_data.get("data_inicial")
        data_final = cleaned_data.get("data_final")

        if data_inicial and data_final:
            if data_final < data_inicial:
                raise forms.ValidationError(
                    _("A data final deve ser igual ou posterior à data inicial.")
                )

        return cleaned_data