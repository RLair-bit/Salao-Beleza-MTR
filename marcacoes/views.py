from datetime import datetime, time, timedelta

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import MarcacaoForm
from .models import Marcacao


def agenda(request):
    dia_txt = request.GET.get("dia")
    try:
        dia = datetime.strptime(dia_txt, "%Y-%m-%d").date() if dia_txt else timezone.localdate()
    except ValueError:
        dia = timezone.localdate()

    inicio_dia = datetime.combine(dia, time.min)
    fim_dia = inicio_dia + timedelta(days=1)
    if settings.USE_TZ:
        inicio_dia = timezone.make_aware(inicio_dia)
        fim_dia = timezone.make_aware(fim_dia)

    marcacoes = (
        Marcacao.objects
        .filter(inicio__gte=inicio_dia, inicio__lt=fim_dia)
        .select_related("cliente", "funcionario", "servico")
    )
    return render(request, "marcacoes/agenda.html", {"marcacoes": marcacoes, "dia": dia})


def criar(request):
    form = MarcacaoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Marcação criada com sucesso.")
        return redirect("marcacoes:agenda")
    return render(request, "marcacoes/form.html", {"form": form, "titulo": "Nova marcação"})