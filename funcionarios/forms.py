from django import forms
from .models import Funcionario


class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ["nome", "telefone", "funcao", "servicos", "ativo"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "telefone": forms.TextInput(attrs={"class": "form-control"}),
            "funcao": forms.TextInput(attrs={"class": "form-control"}),
            "servicos": forms.CheckboxSelectMultiple(),
            "ativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }