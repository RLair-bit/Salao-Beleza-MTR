from .permissoes import (
    e_administrador,
    e_funcionario,
    e_recepcao,
    pode_gerir_operacao,
)


def permissoes_utilizador(request):
    """
    Disponibiliza as permissões do utilizador
    em todos os templates do projeto.
    """
    utilizador = request.user

    return {
        "utilizador_e_administrador": e_administrador(
            utilizador
        ),
        "utilizador_e_recepcao": e_recepcao(
            utilizador
        ),
        "utilizador_e_funcionario": e_funcionario(
            utilizador
        ),
        "utilizador_pode_gerir_operacao": (
            pode_gerir_operacao(utilizador)
        ),
    }