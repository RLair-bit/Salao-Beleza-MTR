from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models.deletion import ProtectedError
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.utils import timezone
from django.utils.translation import gettext as _

from .forms import (
    AusenciaFuncionarioForm,
    FuncionarioForm,
    HorarioTrabalhoCriarForm,
    HorarioTrabalhoForm,
)
from .models import (
    AusenciaFuncionario,
    Funcionario,
    HorarioTrabalho,
)


@login_required
def lista(request):
    procura = request.GET.get(
        "q",
        "",
    ).strip()

    estado = request.GET.get(
        "estado",
        "",
    ).strip()

    funcionarios = (
        Funcionario.objects
        .prefetch_related(
            "servicos",
            "horarios",
        )
        .order_by("nome")
    )

    if procura:
        funcionarios = funcionarios.filter(
            nome__icontains=procura
        )

    if estado == "ativo":
        funcionarios = funcionarios.filter(
            ativo=True
        )

    elif estado == "inativo":
        funcionarios = funcionarios.filter(
            ativo=False
        )

    return render(
        request,
        "funcionarios/lista.html",
        {
            "funcionarios": funcionarios,
            "procura": procura,
            "estado": estado,
        },
    )


@login_required
def detalhe(request, pk):
    funcionario = get_object_or_404(
        Funcionario.objects.prefetch_related(
            "servicos",
            "horarios",
            "ausencias",
        ),
        pk=pk,
    )

    agora = timezone.now()
    hoje = timezone.localdate()

    marcacoes = funcionario.marcacoes.all()

    total_marcacoes = marcacoes.count()

    total_proximas = marcacoes.filter(
        estado="marcada",
        inicio__gte=agora,
    ).count()

    total_realizadas = marcacoes.filter(
        estado="realizada",
    ).count()

    total_canceladas = marcacoes.filter(
        estado="cancelada",
    ).count()

    total_faltas = marcacoes.filter(
        estado="faltou",
    ).count()

    proximas_marcacoes_query = (
        marcacoes
        .filter(
            estado="marcada",
            inicio__gte=agora,
        )
        .select_related(
            "cliente",
            "servico",
            "posto",
        )
        .order_by("inicio")
    )

    proxima_marcacao = (
        proximas_marcacoes_query.first()
    )

    proximas_marcacoes = (
        proximas_marcacoes_query[:5]
    )

    horarios = funcionario.horarios.order_by(
        "dia_semana"
    )

    proximas_ausencias = (
        funcionario.ausencias
        .filter(
            data_fim__gte=hoje,
        )
        .order_by(
            "data_inicio",
            "hora_inicio",
        )[:5]
    )

    return render(
        request,
        "funcionarios/detalhe.html",
        {
            "funcionario": funcionario,
            "total_marcacoes": total_marcacoes,
            "total_proximas": total_proximas,
            "total_realizadas": total_realizadas,
            "total_canceladas": total_canceladas,
            "total_faltas": total_faltas,
            "proxima_marcacao": proxima_marcacao,
            "proximas_marcacoes": proximas_marcacoes,
            "horarios": horarios,
            "proximas_ausencias": proximas_ausencias,
        },
    )


@login_required
def criar(request):
    form = FuncionarioForm(
        request.POST or None,
        request.FILES or None,
    )

    if request.method == "POST" and form.is_valid():
        funcionario = form.save()

        messages.success(
            request,
            _("Funcionário criado com sucesso."),
        )

        return redirect(
            "funcionarios:detalhe",
            pk=funcionario.pk,
        )

    return render(
        request,
        "funcionarios/form.html",
        {
            "form": form,
            "titulo": _("Novo funcionário"),
        },
    )


@login_required
def editar(request, pk):
    funcionario = get_object_or_404(
        Funcionario,
        pk=pk,
    )

    form = FuncionarioForm(
        request.POST or None,
        request.FILES or None,
        instance=funcionario,
    )

    if request.method == "POST" and form.is_valid():
        form.save()

        messages.success(
            request,
            _("Funcionário atualizado."),
        )

        return redirect(
            "funcionarios:detalhe",
            pk=funcionario.pk,
        )

    return render(
        request,
        "funcionarios/form.html",
        {
            "form": form,
            "titulo": _("Editar %(nome)s")
            % {
                "nome": funcionario.nome,
            },
            "funcionario": funcionario,
        },
    )


@login_required
def eliminar(request, pk):
    funcionario = get_object_or_404(
        Funcionario,
        pk=pk,
    )

    if request.method == "POST":
        try:
            funcionario.delete()

            messages.success(
                request,
                _("Funcionário eliminado."),
            )

        except ProtectedError:
            messages.error(
                request,
                _(
                    "Não é possível eliminar: este "
                    "funcionário tem marcações associadas. "
                    "Em alternativa, desative-o."
                ),
            )

        return redirect(
            "funcionarios:lista"
        )

    return render(
        request,
        "funcionarios/confirmar_eliminar.html",
        {
            "funcionario": funcionario,
        },
    )


# ==========================================================
# HORÁRIOS DE TRABALHO
# ==========================================================


@login_required
def horarios_lista(request, funcionario_pk):
    funcionario = get_object_or_404(
        Funcionario,
        pk=funcionario_pk,
    )

    horarios = (
        funcionario.horarios
        .all()
        .order_by("dia_semana")
    )

    return render(
        request,
        "funcionarios/horarios_lista.html",
        {
            "funcionario": funcionario,
            "horarios": horarios,
        },
    )


@login_required
def horario_criar(request, funcionario_pk):
    funcionario = get_object_or_404(
        Funcionario,
        pk=funcionario_pk,
    )

    form = HorarioTrabalhoCriarForm(
        request.POST or None,
        funcionario=funcionario,
    )

    if request.method == "POST" and form.is_valid():
        dados = form.cleaned_data
        dias_semana = dados["dias_semana"]

        with transaction.atomic():
            for dia_semana in dias_semana:
                HorarioTrabalho.objects.create(
                    funcionario=funcionario,
                    dia_semana=int(dia_semana),
                    hora_inicio=dados["hora_inicio"],
                    hora_fim=dados["hora_fim"],
                    intervalo_inicio=dados[
                        "intervalo_inicio"
                    ],
                    intervalo_fim=dados[
                        "intervalo_fim"
                    ],
                    ativo=dados["ativo"],
                )

        messages.success(
            request,
            _(
                "Os horários de trabalho foram "
                "criados com sucesso."
            ),
        )

        return redirect(
            "funcionarios:horarios_lista",
            funcionario_pk=funcionario.pk,
        )

    return render(
        request,
        "funcionarios/horario_form.html",
        {
            "form": form,
            "funcionario": funcionario,
            "titulo": _("Adicionar horários"),
            "criacao_multipla": True,
        },
    )


@login_required
def horario_editar(request, pk):
    horario = get_object_or_404(
        HorarioTrabalho.objects.select_related(
            "funcionario"
        ),
        pk=pk,
    )

    form = HorarioTrabalhoForm(
        request.POST or None,
        instance=horario,
    )

    if request.method == "POST" and form.is_valid():
        form.save()

        messages.success(
            request,
            _("Horário de trabalho atualizado."),
        )

        return redirect(
            "funcionarios:horarios_lista",
            funcionario_pk=horario.funcionario.pk,
        )

    return render(
        request,
        "funcionarios/horario_form.html",
        {
            "form": form,
            "funcionario": horario.funcionario,
            "horario": horario,
            "titulo": _("Editar horário"),
            "criacao_multipla": False,
        },
    )


@login_required
def horario_eliminar(request, pk):
    horario = get_object_or_404(
        HorarioTrabalho.objects.select_related(
            "funcionario"
        ),
        pk=pk,
    )

    funcionario = horario.funcionario

    if request.method == "POST":
        horario.delete()

        messages.success(
            request,
            _("Horário de trabalho eliminado."),
        )

        return redirect(
            "funcionarios:horarios_lista",
            funcionario_pk=funcionario.pk,
        )

    return render(
        request,
        "funcionarios/horario_confirmar_eliminar.html",
        {
            "horario": horario,
            "funcionario": funcionario,
        },
    )


# ==========================================================
# AUSÊNCIAS, FOLGAS E FÉRIAS
# ==========================================================


@login_required
def ausencias_lista(request, funcionario_pk):
    funcionario = get_object_or_404(
        Funcionario,
        pk=funcionario_pk,
    )

    ausencias = (
        funcionario.ausencias
        .all()
        .order_by(
            "-data_inicio",
            "-hora_inicio",
        )
    )

    return render(
        request,
        "funcionarios/ausencias_lista.html",
        {
            "funcionario": funcionario,
            "ausencias": ausencias,
        },
    )


@login_required
def ausencia_criar(request, funcionario_pk):
    funcionario = get_object_or_404(
        Funcionario,
        pk=funcionario_pk,
    )

    form = AusenciaFuncionarioForm(
        request.POST or None,
        initial={
            "data_inicio": timezone.localdate(),
            "data_fim": timezone.localdate(),
            "dia_inteiro": True,
        },
    )

    form.instance.funcionario = funcionario

    if request.method == "POST" and form.is_valid():
        ausencia = form.save(
            commit=False
        )

        ausencia.funcionario = funcionario
        ausencia.save()

        messages.success(
            request,
            _("Ausência registada com sucesso."),
        )

        return redirect(
            "funcionarios:ausencias_lista",
            funcionario_pk=funcionario.pk,
        )

    return render(
        request,
        "funcionarios/ausencia_form.html",
        {
            "form": form,
            "funcionario": funcionario,
            "titulo": _("Registar ausência"),
        },
    )


@login_required
def ausencia_editar(request, pk):
    ausencia = get_object_or_404(
        AusenciaFuncionario.objects.select_related(
            "funcionario"
        ),
        pk=pk,
    )

    form = AusenciaFuncionarioForm(
        request.POST or None,
        instance=ausencia,
    )

    if request.method == "POST" and form.is_valid():
        form.save()

        messages.success(
            request,
            _("Ausência atualizada."),
        )

        return redirect(
            "funcionarios:ausencias_lista",
            funcionario_pk=ausencia.funcionario.pk,
        )

    return render(
        request,
        "funcionarios/ausencia_form.html",
        {
            "form": form,
            "funcionario": ausencia.funcionario,
            "ausencia": ausencia,
            "titulo": _("Editar ausência"),
        },
    )


@login_required
def ausencia_eliminar(request, pk):
    ausencia = get_object_or_404(
        AusenciaFuncionario.objects.select_related(
            "funcionario"
        ),
        pk=pk,
    )

    funcionario = ausencia.funcionario

    if request.method == "POST":
        ausencia.delete()

        messages.success(
            request,
            _("Ausência eliminada."),
        )

        return redirect(
            "funcionarios:ausencias_lista",
            funcionario_pk=funcionario.pk,
        )

    return render(
        request,
        "funcionarios/ausencia_confirmar_eliminar.html",
        {
            "ausencia": ausencia,
            "funcionario": funcionario,
        },
    )