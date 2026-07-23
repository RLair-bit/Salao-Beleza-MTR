from django import forms

from servicos.models import Servico


class ServicoForm(forms.ModelForm):

    class Meta:
        model = Servico
        fields = ["nome", "descricao", "preco"]

        widgets = {
            "nome": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nome do serviço",
                "autofocus": True,
            }),

            "preco": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Preço do serviço",
                "step": 0.01,
            }),

            "duracao_min": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Duração do serviço (minutos)",
                "step": 5,
            }),

            "ativo": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),
        }