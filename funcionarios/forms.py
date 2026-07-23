from django import forms

from .models import Funcionario


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
                    "accept": "image/*",
                }
            ),
            "nome": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "telefone": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "funcao": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "servicos": forms.CheckboxSelectMultiple(),
            "ativo": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }