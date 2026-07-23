from datetime import datetime, time, timedelta

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from marcacoes.models import Marcacao

from .forms import (
    UtilizadorCriarForm,
    UtilizadorEditarForm,
)
from .permissoes import (
    e_funcionario,
    exigir_administrador,
    exigir_funcionario_associado,
    pode_gerir_operacao,
)


User = get_user_model()


def proteger_superutilizador(request, utilizador):
    """
    Impede que um administrador comum altere
    uma conta superutilizadora.
    """
    if (
        utilizador.is_superuser
        and not request.user.is_superuser
    ):
        raise PermissionDenied(
            _(
                "Apenas um superutilizador pode "
                "alterar esta conta."
            )
        )


@login_required
def lista(request):
    """
    Mostra a lista de utilizadores.

    Apenas superutilizadores e membros do grupo
    Administrador podem aceder.
    """
    exigir_administrador(request.user)

    procura = request.GET.get(
        "q",
        "",
    ).strip()

    grupo = request.GET.get(
        "grupo",
        "",
    ).strip()

    estado = request.GET.get(
        "estado",
        "",
    ).strip()

    utilizadores = (
        User.objects
        .select_related("funcionario")
        .prefetch_related("groups")
        .order_by("username")
    )

    if procura:
        utilizadores = utilizadores.filter(
            Q(username__icontains=procura)
            | Q(first_name__icontains=procura)
            | Q(last_name__icontains=procura)
            | Q(email__icontains=procura)
        )

    if grupo:
        utilizadores = utilizadores.filter(
            groups__name=grupo
        )

    if estado == "ativo":
        utilizadores = utilizadores.filter(
            is_active=True
        )

    elif estado == "inativo":
        utilizadores = utilizadores.filter(
            is_active=False
        )

    utilizadores = utilizadores.distinct()

    return render(
        request,
        "utilizadores/lista.html",
        {
            "utilizadores": utilizadores,
            "procura": procura,
            "grupo_escolhido": grupo,
            "estado": estado,
            "grupos": [
                "Administrador",
                "Receção",
                "Funcionário",
            ],
        },
    )


@login_required
def criar(request):
    """
    Cria uma nova conta de utilizador.
    """
    exigir_administrador(request.user)

    form = UtilizadorCriarForm(
        request.POST or None
    )

    if request.method == "POST" and form.is_valid():
        utilizador = form.save()

        messages.success(
            request,
            _(
                "O utilizador %(username)s foi criado "
                "com sucesso."
            )
            % {
                "username": utilizador.username,
            },
        )

        return redirect(
            "utilizadores:lista"
        )

    return render(
        request,
        "utilizadores/form.html",
        {
            "form": form,
            "titulo": _("Novo utilizador"),
            "modo_criacao": True,
        },
    )


@login_required
def editar(request, pk):
    """
    Altera os dados, o grupo, o funcionário associado
    e o estado de uma conta.
    """
    exigir_administrador(request.user)

    utilizador = get_object_or_404(
        User,
        pk=pk,
    )

    proteger_superutilizador(
        request,
        utilizador,
    )

    form = UtilizadorEditarForm(
        request.POST or None,
        instance=utilizador,
    )

    if request.method == "POST" and form.is_valid():
        pretende_desativar_propria_conta = (
            utilizador == request.user
            and not form.cleaned_data["is_active"]
        )

        if pretende_desativar_propria_conta:
            form.add_error(
                "is_active",
                _(
                    "Não pode desativar a própria conta."
                ),
            )

        else:
            form.save()

            messages.success(
                request,
                _(
                    "O utilizador %(username)s "
                    "foi atualizado."
                )
                % {
                    "username": utilizador.username,
                },
            )

            return redirect(
                "utilizadores:lista"
            )

    return render(
        request,
        "utilizadores/form.html",
        {
            "form": form,
            "titulo": _("Editar utilizador"),
            "utilizador_editado": utilizador,
            "modo_criacao": False,
        },
    )


@login_required
@require_POST
def alterar_estado(request, pk):
    """
    Ativa ou desativa uma conta sem a eliminar.
    """
    exigir_administrador(request.user)

    utilizador = get_object_or_404(
        User,
        pk=pk,
    )

    proteger_superutilizador(
        request,
        utilizador,
    )

    if utilizador == request.user:
        messages.error(
            request,
            _(
                "Não pode desativar a própria conta."
            ),
        )

        return redirect(
            "utilizadores:lista"
        )

    utilizador.is_active = not utilizador.is_active

    utilizador.save(
        update_fields=["is_active"]
    )

    if utilizador.is_active:
        mensagem = _(
            "A conta de %(username)s foi ativada."
        )
    else:
        mensagem = _(
            "A conta de %(username)s foi desativada."
        )

    messages.success(
        request,
        mensagem
        % {
            "username": utilizador.username,
        },
    )

    return redirect(
        "utilizadores:lista"
    )


@login_required
def minha_agenda(request):
    """
    O funcionário consulta apenas a própria agenda.

    Administradores e Receção são encaminhados
    para a agenda geral do salão.
    """
    if pode_gerir_operacao(request.user):
        return redirect(
            "marcacoes:agenda"
        )

    if not e_funcionario(request.user):
        raise PermissionDenied(
            _(
                "Não tem permissão para consultar "
                "esta agenda."
            )
        )

    funcionario = exigir_funcionario_associado(
        request.user
    )

    data_texto = request.GET.get(
        "data",
        "",
    ).strip()

    estado = request.GET.get(
        "estado",
        "",
    ).strip()

    if data_texto:
        data_escolhida = parse_date(
            data_texto
        )

        if data_escolhida is None:
            messages.error(
                request,
                _("A data indicada não é válida."),
            )

            data_escolhida = timezone.localdate()

    else:
        data_escolhida = timezone.localdate()

    fuso_horario = timezone.get_current_timezone()

    inicio_dia = timezone.make_aware(
        datetime.combine(
            data_escolhida,
            time.min,
        ),
        timezone=fuso_horario,
    )

    data_dia_seguinte = (
        data_escolhida
        + timedelta(days=1)
    )

    fim_dia = timezone.make_aware(
        datetime.combine(
            data_dia_seguinte,
            time.min,
        ),
        timezone=fuso_horario,
    )

    marcacoes = (
        Marcacao.objects
        .filter(
            funcionario=funcionario,
            inicio__gte=inicio_dia,
            inicio__lt=fim_dia,
        )
        .select_related(
            "cliente",
            "funcionario",
            "servico",
            "posto",
        )
        .order_by("inicio")
    )

    estados_validos = dict(
        Marcacao.ESTADOS
    )

    if estado in estados_validos:
        marcacoes = marcacoes.filter(
            estado=estado
        )
    else:
        estado = ""

    return render(
        request,
        "utilizadores/minha_agenda.html",
        {
            "funcionario": funcionario,
            "marcacoes": marcacoes,
            "data_escolhida": data_escolhida,
            "estado_escolhido": estado,
            "estados": Marcacao.ESTADOS,
            "hoje": timezone.localdate(),
        },
    )


@login_required
def meu_perfil(request):
    """
    Mostra os dados profissionais e da conta
    do funcionário autenticado.
    """
    if not e_funcionario(request.user):
        raise PermissionDenied(
            _(
                "Esta página está disponível apenas "
                "para funcionários."
            )
        )

    funcionario = exigir_funcionario_associado(
        request.user
    )

    servicos = funcionario.servicos.all()

    return render(
        request,
        "utilizadores/meu_perfil.html",
        {
            "funcionario": funcionario,
            "servicos": servicos,
        },
    )