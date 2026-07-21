from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = [ "nome", "telefone", "email", ]

        widgets = {
            "nome": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nome completo",
                "autofocus": True,
            }),

            "telefone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "(11) 99999-9999",
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "cliente@email.com",
            }),
        }