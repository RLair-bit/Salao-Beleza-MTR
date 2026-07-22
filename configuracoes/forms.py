from django import forms

from .models import Configuracao


class ConfiguracaoForm(forms.ModelForm):
    class Meta:
        model = Configuracao
        fields = ["nome_salao", "telefone", "email", "morada",
                  "hora_abertura", "hora_fecho", "idioma", "fuso_horario"]
        widgets = {
            "nome_salao": forms.TextInput(attrs={"class": "form-control", "autofocus": True}),
            "telefone": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "morada": forms.TextInput(attrs={"class": "form-control"}),
            "hora_abertura": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "hora_fecho": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "idioma": forms.Select(attrs={"class": "form-select"}),
            "fuso_horario": forms.Select(attrs={"class": "form-select"}),
        }