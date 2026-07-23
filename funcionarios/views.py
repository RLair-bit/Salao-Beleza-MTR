from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models.deletion import ProtectedError
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.utils import timezone
from django.utils.translation import gettext as _

from .forms import FuncionarioForm
from .models import Funcionario


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
        .prefetch_related("servicos")
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
            "servicos"
        ),
        pk=pk,
    )

    agora = timezone.now()

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

    proxima_marcacao = proximas_marcacoes_query.first()

    proximas_marcacoes = proximas_marcacoes_query[:5]

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
        },
    )


@login_required
def criar(request):
    form = FuncionarioForm(
        request.POST or None,
        request.FILES or None,
    )

    if request.method == "POST" and form.is_valid():
        form.save()

        messages.success(
            request,
            _("Funcionário criado com sucesso."),
        )

        return redirect(
            "funcionarios:lista"
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
            "funcionarios:lista"
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