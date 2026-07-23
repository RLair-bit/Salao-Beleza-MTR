from django.core.exceptions import (
    ObjectDoesNotExist,
    PermissionDenied,
)
from django.utils.translation import gettext as _


GRUPO_ADMINISTRADOR = "Administrador"
GRUPO_RECECAO = "Receção"
GRUPO_FUNCIONARIO = "Funcionário"


def utilizador_valido(utilizador):
    """
    Confirma se a conta está autenticada e ativa.
    """
    return (
        utilizador.is_authenticated
        and utilizador.is_active
    )


def pertence_ao_grupo(utilizador, nome_do_grupo):
    """
    Verifica se o utilizador pertence ao grupo indicado.
    """
    return (
        utilizador_valido(utilizador)
        and utilizador.groups.filter(
            name=nome_do_grupo
        ).exists()
    )


def e_administrador(utilizador):
    """
    Um superutilizador ou membro do grupo Administrador
    tem acesso administrativo.
    """
    return (
        utilizador_valido(utilizador)
        and (
            utilizador.is_superuser
            or pertence_ao_grupo(
                utilizador,
                GRUPO_ADMINISTRADOR,
            )
        )
    )


def e_recepcao(utilizador):
    """
    Verifica se o utilizador pertence ao grupo Receção.
    """
    return pertence_ao_grupo(
        utilizador,
        GRUPO_RECECAO,
    )


def e_funcionario(utilizador):
    """
    Verifica se o utilizador pertence ao grupo Funcionário.
    """
    return pertence_ao_grupo(
        utilizador,
        GRUPO_FUNCIONARIO,
    )


def pode_gerir_operacao(utilizador):
    """
    Administradores e Receção podem trabalhar nas áreas
    operacionais do salão.
    """
    return (
        e_administrador(utilizador)
        or e_recepcao(utilizador)
    )


def pode_ver_todas_as_agendas(utilizador):
    """
    Administradores e Receção podem consultar as agendas
    de todos os funcionários.
    """
    return pode_gerir_operacao(utilizador)


def pode_ver_apenas_a_propria_agenda(utilizador):
    """
    O grupo Funcionário pode consultar apenas a sua agenda.
    """
    return e_funcionario(utilizador)


def funcionario_associado(utilizador):
    """
    Devolve o funcionário associado à conta.

    Quando a conta não estiver ligada a nenhum funcionário,
    devolve None.
    """
    if not utilizador_valido(utilizador):
        return None

    try:
        return utilizador.funcionario
    except ObjectDoesNotExist:
        return None


def exigir_administrador(utilizador):
    """
    Interrompe o acesso quando o utilizador não é
    administrador.
    """
    if not e_administrador(utilizador):
        raise PermissionDenied(
            _(
                "Não tem permissão para aceder "
                "a esta página."
            )
        )


def exigir_recepcao_ou_administrador(utilizador):
    """
    Permite o acesso apenas à Receção e Administradores.
    """
    if not pode_gerir_operacao(utilizador):
        raise PermissionDenied(
            _(
                "Esta área está disponível apenas "
                "para a Receção e Administradores."
            )
        )


def exigir_funcionario_associado(utilizador):
    """
    Confirma que a conta possui um funcionário associado
    e devolve esse funcionário.
    """
    funcionario = funcionario_associado(utilizador)

    if funcionario is None:
        raise PermissionDenied(
            _(
                "Esta conta ainda não está associada "
                "a um funcionário."
            )
        )

    return funcionario