from datetime import datetime, time, timedelta

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from funcionarios.models import Funcionario

from .forms import MarcacaoForm
from .models import Marcacao

from django.db.models import Sum

from clientes.models import Cliente
from servicos.models import Servico

def _dia_de(marcacao):
    """Devolve o dia da marcação no formato usado pelo filtro da agenda."""
    inicio = marcacao.inicio
    if settings.USE_TZ:
        inicio = timezone.localtime(inicio)
    return inicio.strftime("%Y-%m-%d")


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
        .select_related("cliente", "funcionario", "servico", "posto")
    )

    escolhido = request.GET.get("funcionario", "")
    if escolhido.isdigit():
        marcacoes = marcacoes.filter(funcionario_id=int(escolhido))
    else:
        escolhido = ""

    return render(request, "marcacoes/agenda.html", {
        "marcacoes": marcacoes,
        "dia": dia,
        "dia_anterior": dia - timedelta(days=1),
        "dia_seguinte": dia + timedelta(days=1),
        "hoje": timezone.localdate(),
        "funcionarios": Funcionario.objects.filter(ativo=True),
        "escolhido": escolhido,
        "total": marcacoes.count(),
    })


def criar(request):
    form = MarcacaoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Marcação criada com sucesso.")
        return redirect("marcacoes:agenda")
    return render(request, "marcacoes/form.html", {"form": form, "titulo": "Nova marcação"})


def editar(request, pk):
    marcacao = get_object_or_404(Marcacao, pk=pk)
    form = MarcacaoForm(request.POST or None, instance=marcacao)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Marcação atualizada.")
        return redirect(f"{reverse('marcacoes:agenda')}?dia={_dia_de(marcacao)}")
    return render(request, "marcacoes/form.html",
                  {"form": form, "titulo": "Editar marcação"})


def mudar_estado(request, pk, estado):
    marcacao = get_object_or_404(Marcacao, pk=pk)
    validos = dict(Marcacao.ESTADOS)
    dia = _dia_de(marcacao)

    if request.method == "POST" and estado in validos:
        marcacao.estado = estado
        try:
            marcacao.save()
            messages.success(request, f"Marcação alterada para {validos[estado]}.")
        except ValidationError as e:
            messages.error(request, e.messages[0])

    return redirect(f"{reverse('marcacoes:agenda')}?dia={dia}")

def painel(request):
    hoje = timezone.localdate()
    inicio = datetime.combine(hoje, time.min)
    fim = inicio + timedelta(days=1)
    if settings.USE_TZ:
        inicio = timezone.make_aware(inicio)
        fim = timezone.make_aware(fim)

    do_dia = (Marcacao.objects
              .filter(inicio__gte=inicio, inicio__lt=fim)
              .exclude(estado="cancelada")
              .select_related("cliente", "funcionario", "servico", "posto"))

    realizadas = do_dia.filter(estado="realizada")
    agora = timezone.now()
    proximas = [m for m in do_dia if m.inicio >= agora and m.estado == "marcada"][:5]

    return render(request, "home.html", {
        "hoje": hoje,
        "total_dia": do_dia.count(),
        "n_realizadas": realizadas.count(),
        "receita": realizadas.aggregate(t=Sum("servico__preco"))["t"] or 0,
        "proximas": proximas,
        "n_clientes": Cliente.objects.count(),
        "n_servicos": Servico.objects.filter(ativo=True).count(),
        "n_funcionarios": Funcionario.objects.filter(ativo=True).count(),
    })