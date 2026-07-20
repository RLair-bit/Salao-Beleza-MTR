from django import forms

from .models import Marcacao


class MarcacaoForm(forms.ModelForm):
    class Meta:
        model = Marcacao
        fields = ["cliente", "funcionario", "servico", "posto", "inicio", "estado", "notas"]
        widgets = {
            "inicio": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
            "cliente": forms.Select(attrs={"class": "form-select"}),
            "funcionario": forms.Select(attrs={"class": "form-select"}),
            "servico": forms.Select(attrs={"class": "form-select"}),
            "posto": forms.Select(attrs={"class": "form-select"}),
            "estado": forms.Select(attrs={"class": "form-select"}),
            "notas": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["inicio"].input_formats = ["%Y-%m-%dT%H:%M"]