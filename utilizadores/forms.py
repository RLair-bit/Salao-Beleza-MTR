from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from funcionarios.models import Funcionario


User = get_user_model()


NOMES_DOS_GRUPOS = [
    "Administrador",
    "Receção",
    "Funcionário",
]


def aplicar_estilo_aos_campos(formulario):
    for campo in formulario.fields.values():
        if isinstance(campo.widget, forms.CheckboxInput):
            campo.widget.attrs["class"] = "form-check-input"

        elif isinstance(
            campo.widget,
            (
                forms.Select,
                forms.SelectMultiple,
            ),
        ):
            campo.widget.attrs["class"] = "form-select"

        else:
            campo.widget.attrs["class"] = "form-control"


class UtilizadorCriarForm(UserCreationForm):
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.none(),
        label=_("Grupo de acesso"),
        empty_label=_("Selecione um grupo"),
    )

    funcionario = forms.ModelChoiceField(
        queryset=Funcionario.objects.none(),
        label=_("Funcionário associado"),
        required=False,
        empty_label=_("Nenhum funcionário associado"),
    )

    class Meta(UserCreationForm.Meta):
        model = User

        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "is_active",
        )

        labels = {
            "username": _("Utilizador"),
            "first_name": _("Nome"),
            "last_name": _("Apelido"),
            "email": _("Email"),
            "is_active": _("Conta ativa"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["grupo"].queryset = (
            Group.objects
            .filter(name__in=NOMES_DOS_GRUPOS)
            .order_by("name")
        )

        self.fields["funcionario"].queryset = (
            Funcionario.objects
            .filter(utilizador__isnull=True)
            .order_by("nome")
        )

        self.order_fields(
            [
                "username",
                "first_name",
                "last_name",
                "email",
                "grupo",
                "funcionario",
                "is_active",
                "password1",
                "password2",
            ]
        )

        aplicar_estilo_aos_campos(self)

    def save(self, commit=True):
        utilizador = super().save(commit=commit)

        if commit:
            grupo = self.cleaned_data["grupo"]
            funcionario = self.cleaned_data.get("funcionario")

            utilizador.groups.set([grupo])

            if funcionario:
                funcionario.utilizador = utilizador

                funcionario.save(
                    update_fields=["utilizador"]
                )

        return utilizador


class UtilizadorEditarForm(forms.ModelForm):
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.none(),
        label=_("Grupo de acesso"),
        empty_label=_("Selecione um grupo"),
    )

    funcionario = forms.ModelChoiceField(
        queryset=Funcionario.objects.none(),
        label=_("Funcionário associado"),
        required=False,
        empty_label=_("Nenhum funcionário associado"),
    )

    class Meta:
        model = User

        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "is_active",
        )

        labels = {
            "username": _("Utilizador"),
            "first_name": _("Nome"),
            "last_name": _("Apelido"),
            "email": _("Email"),
            "is_active": _("Conta ativa"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        grupo_atual = (
            self.instance.groups
            .filter(name__in=NOMES_DOS_GRUPOS)
            .first()
        )

        funcionario_atual = (
            Funcionario.objects
            .filter(utilizador=self.instance)
            .first()
        )

        self.fields["grupo"].queryset = (
            Group.objects
            .filter(name__in=NOMES_DOS_GRUPOS)
            .order_by("name")
        )

        self.fields["funcionario"].queryset = (
            Funcionario.objects
            .filter(
                Q(utilizador__isnull=True)
                | Q(utilizador=self.instance)
            )
            .order_by("nome")
        )

        if grupo_atual:
            self.fields["grupo"].initial = grupo_atual

        if funcionario_atual:
            self.fields["funcionario"].initial = (
                funcionario_atual
            )

        self.order_fields(
            [
                "username",
                "first_name",
                "last_name",
                "email",
                "grupo",
                "funcionario",
                "is_active",
            ]
        )

        aplicar_estilo_aos_campos(self)

    def save(self, commit=True):
        utilizador = super().save(commit=commit)

        if commit:
            grupo = self.cleaned_data["grupo"]
            funcionario = self.cleaned_data.get("funcionario")

            utilizador.groups.set([grupo])

            Funcionario.objects.filter(
                utilizador=utilizador
            ).update(
                utilizador=None
            )

            if funcionario:
                funcionario.utilizador = utilizador

                funcionario.save(
                    update_fields=["utilizador"]
                )

        return utilizador