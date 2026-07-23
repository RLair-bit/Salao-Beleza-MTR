from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from marcacoes.views import painel

from .permissoes import e_funcionario


@login_required
def inicio(request):
    """
    Define a página inicial conforme o grupo da conta.

    Funcionários são encaminhados para a própria agenda.
    Administradores e Receção continuam no painel geral.
    """
    if e_funcionario(request.user):
        return redirect(
            "utilizadores:minha_agenda"
        )

    return painel(request)