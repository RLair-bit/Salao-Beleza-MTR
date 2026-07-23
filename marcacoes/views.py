from datetime import datetime, time, timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Q, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _

from clientes.models import Cliente
from funcionarios.models import Funcionario
from servicos.models import Servico

from .forms import MarcacaoForm
from .models import Marcacao


def _tornar_aware(valor):
    """
    Acrescenta o fuso horário definido no Django a uma data
    que ainda não tenha informação de fuso horário.
    """
    if settings.USE_TZ and timezone.is_naive(valor):
        return timezone.make_aware(
            valor,
            timezone.get_current_timezone(),
        )

    return valor


def _dia_de(marcacao):
    """
    Devolve o dia da marcação no formato usado pelo filtro
    da agenda.
    """
    inicio = marcacao.inicio

    if settings.USE_TZ:
        inicio = timezone.localtime(inicio)

    return inicio.strftime("%Y-%m-%d")


@login_required
def agenda(request):
    dia_txt = request.GET.get("dia")

    try:
        if dia_txt:
            dia = datetime.strptime(
                dia_txt,
                "%Y-%m-%d",
            ).date()
        else:
            dia = timezone.localdate()
    except ValueError:
        dia = timezone.localdate()

    inicio_dia = _tornar_aware(
        datetime.combine(dia, time.min)
    )

    fim_dia = inicio_dia + timedelta(days=1)

    marcacoes = (
        Marcacao.objects
        .filter(
            inicio__gte=inicio_dia,
            inicio__lt=fim_dia,
        )
        .select_related(
            "cliente",
            "funcionario",
            "servico",
            "posto",
        )
    )

    escolhido = request.GET.get("funcionario", "")

    if escolhido.isdigit():
        marcacoes = marcacoes.filter(
            funcionario_id=int(escolhido)
        )
    else:
        escolhido = ""

    return render(
        request,
        "marcacoes/agenda.html",
        {
            "marcacoes": marcacoes,
            "dia": dia,
            "dia_anterior": dia - timedelta(days=1),
            "dia_seguinte": dia + timedelta(days=1),
            "hoje": timezone.localdate(),
            "funcionarios": Funcionario.objects.filter(
                ativo=True
            ),
            "escolhido": escolhido,
            "total": marcacoes.count(),
        },
    )


@login_required
def horarios_disponiveis(request):
    """
    Calcula os horários disponíveis entre as 09:00 e as
    19:00, em intervalos de 30 minutos.
    """
    funcionario_txt = request.GET.get("funcionario", "")
    servico_txt = request.GET.get("servico", "")
    posto_txt = request.GET.get("posto", "")
    dia_txt = request.GET.get("dia", "")
    marcacao_txt = request.GET.get("marcacao", "")

    if not funcionario_txt.isdigit():
        return JsonResponse(
            {"erro": _("Selecione um funcionário.")},
            status=400,
        )

    if not servico_txt.isdigit():
        return JsonResponse(
            {"erro": _("Selecione um serviço.")},
            status=400,
        )

    try:
        dia = datetime.strptime(
            dia_txt,
            "%Y-%m-%d",
        ).date()
    except ValueError:
        return JsonResponse(
            {"erro": _("Selecione uma data válida.")},
            status=400,
        )

    funcionario_id = int(funcionario_txt)
    servico_id = int(servico_txt)

    posto_id = (
        int(posto_txt)
        if posto_txt.isdigit()
        else None
    )

    marcacao_id = (
        int(marcacao_txt)
        if marcacao_txt.isdigit()
        else None
    )

    funcionario_existe = Funcionario.objects.filter(
        pk=funcionario_id
    ).exists()

    if not funcionario_existe:
        return JsonResponse(
            {"erro": _("Funcionário não encontrado.")},
            status=404,
        )

    servico = Servico.objects.filter(
        pk=servico_id
    ).first()

    if servico is None:
        return JsonResponse(
            {"erro": _("Serviço não encontrado.")},
            status=404,
        )

    if servico.duracao_min <= 0:
        return JsonResponse(
            {"erro": _("A duração do serviço é inválida.")},
            status=400,
        )

    abertura = _tornar_aware(
        datetime.combine(dia, time(9, 0))
    )

    fecho = _tornar_aware(
        datetime.combine(dia, time(19, 0))
    )

    filtro_recursos = Q(
        funcionario_id=funcionario_id
    )

    if posto_id is not None:
        filtro_recursos |= Q(
            posto_id=posto_id
        )

    marcacoes_existentes = (
        Marcacao.objects
        .filter(filtro_recursos)
        .filter(
            inicio__gte=abertura - timedelta(hours=12),
            inicio__lt=fecho,
        )
        .exclude(estado="cancelada")
        .select_related(
            "servico",
            "funcionario",
            "posto",
        )
    )

    if marcacao_id is not None:
        marcacoes_existentes = (
            marcacoes_existentes.exclude(
                pk=marcacao_id
            )
        )

    marcacoes_existentes = list(
        marcacoes_existentes
    )

    duracao = timedelta(
        minutes=servico.duracao_min
    )

    intervalo = timedelta(minutes=30)
    horario_atual = abertura
    horarios = []

    if settings.USE_TZ:
        agora = timezone.localtime(
            timezone.now()
        )
    else:
        agora = timezone.now()

    while horario_atual + duracao <= fecho:
        fim_horario = horario_atual + duracao

        horario_passado = (
            dia == timezone.localdate()
            and horario_atual <= agora
        )

        conflito = False

        if not horario_passado:
            for marcacao in marcacoes_existentes:
                existe_sobreposicao = (
                    horario_atual < marcacao.fim
                    and marcacao.inicio < fim_horario
                )

                if not existe_sobreposicao:
                    continue

                mesmo_funcionario = (
                    marcacao.funcionario_id
                    == funcionario_id
                )

                mesmo_posto = (
                    posto_id is not None
                    and marcacao.posto_id == posto_id
                )

                if mesmo_funcionario or mesmo_posto:
                    conflito = True
                    break

        if not horario_passado and not conflito:
            horarios.append(
                {
                    "valor": horario_atual.strftime(
                        "%Y-%m-%dT%H:%M"
                    ),
                    "inicio": horario_atual.strftime(
                        "%H:%M"
                    ),
                    "fim": fim_horario.strftime(
                        "%H:%M"
                    ),
                }
            )

        horario_atual += intervalo

    return JsonResponse(
        {
            "horarios": horarios,
            "duracao": servico.duracao_min,
        }
    )


@login_required
def criar(request):
    form = MarcacaoForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()

        messages.success(
            request,
            _("Marcação criada com sucesso."),
        )

        return redirect("marcacoes:agenda")

    return render(
        request,
        "marcacoes/form.html",
        {
            "form": form,
            "titulo": _("Nova marcação"),
        },
    )


@login_required
def editar(request, pk):
    marcacao = get_object_or_404(
        Marcacao,
        pk=pk,
    )

    form = MarcacaoForm(
        request.POST or None,
        instance=marcacao,
    )

    if request.method == "POST" and form.is_valid():
        form.save()

        messages.success(
            request,
            _("Marcação atualizada."),
        )

        return redirect(
            f"{reverse('marcacoes:agenda')}"
            f"?dia={_dia_de(marcacao)}"
        )

    return render(
        request,
        "marcacoes/form.html",
        {
            "form": form,
            "titulo": _("Editar marcação"),
        },
    )


@login_required
def mudar_estado(request, pk, estado):
    marcacao = get_object_or_404(
        Marcacao,
        pk=pk,
    )

    estados_validos = dict(Marcacao.ESTADOS)
    dia = _dia_de(marcacao)

    if (
        request.method == "POST"
        and estado in estados_validos
    ):
        marcacao.estado = estado

        try:
            marcacao.save()

            messages.success(
                request,
                _("Marcação alterada para %(estado)s.") % {
                    "estado": estados_validos[estado]
                },
            )
        except ValidationError as erro:
            messages.error(
                request,
                erro.messages[0],
            )

    return redirect(
        f"{reverse('marcacoes:agenda')}?dia={dia}"
    )


@login_required
def painel(request):
    hoje = timezone.localdate()

    inicio = _tornar_aware(
        datetime.combine(hoje, time.min)
    )

    fim = inicio + timedelta(days=1)

    do_dia = (
        Marcacao.objects
        .filter(
            inicio__gte=inicio,
            inicio__lt=fim,
        )
        .exclude(estado="cancelada")
        .select_related(
            "cliente",
            "funcionario",
            "servico",
            "posto",
        )
    )

    realizadas = do_dia.filter(
        estado="realizada"
    )

    por_fechar = [
        marcacao
        for marcacao in do_dia
        if marcacao.estado == "marcada"
    ]

    atrasadas = [
        marcacao
        for marcacao in por_fechar
        if marcacao.em_atraso
    ]

    return render(
        request,
        "home.html",
        {
            "hoje": hoje,
            "total_dia": do_dia.count(),
            "n_realizadas": realizadas.count(),
            "receita": (
                realizadas.aggregate(
                    total=Sum("servico__preco")
                )["total"]
                or 0
            ),
            "proximas": por_fechar[:8],
            "n_atrasadas": len(atrasadas),
            "n_clientes": Cliente.objects.count(),
            "n_servicos": Servico.objects.filter(
                ativo=True
            ).count(),
            "n_funcionarios": (
                Funcionario.objects.filter(
                    ativo=True
                ).count()
            ),
        },
    )


@login_required
def pendentes(request):
    """
    Lista as marcações de dias anteriores que ficaram por
    fechar (continuam no estado "marcada").
    """
    inicio_hoje = _tornar_aware(
        datetime.combine(timezone.localdate(), time.min)
    )

    marcacoes = (
        Marcacao.objects
        .filter(
            estado="marcada",
            inicio__lt=inicio_hoje,
        )
        .select_related(
            "cliente",
            "funcionario",
            "servico",
            "posto",
        )
        .order_by("-inicio")
    )

    return render(
        request,
        "marcacoes/pendentes.html",
        {
            "marcacoes": marcacoes,
            "total": marcacoes.count(),
        },
    )
