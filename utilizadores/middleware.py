from urllib.parse import urlencode

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import Resolver404, resolve
from django.utils.translation import gettext as _

from .permissoes import (
    e_administrador,
    e_funcionario,
    e_recepcao,
)


class ControloAcessoMiddleware:
    """
    Controla o acesso às páginas conforme o grupo
    do utilizador autenticado.

    Administrador:
        Acesso completo à aplicação.

    Receção:
        Acesso às áreas operacionais do salão.

    Funcionário:
        Acesso apenas à própria agenda e ao próprio perfil.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        resposta = self.verificar_acesso(request)

        if resposta is not None:
            return resposta

        return self.get_response(request)

    @staticmethod
    def prefixo(valor):
        """
        Garante que o endereço começa com uma barra.
        """
        return "/" + valor.lstrip("/")

    def caminho_publico(self, request):
        """
        Endereços que não devem ser bloqueados pelo
        middleware.
        """
        caminhos_publicos = [
            self.prefixo(settings.STATIC_URL),
            self.prefixo(settings.MEDIA_URL),
            "/contas/",
            "/favicon.ico",
        ]

        return any(
            request.path_info.startswith(caminho)
            for caminho in caminhos_publicos
        )

    @staticmethod
    def enviar_para_login(request):
        """
        Envia uma pessoa não autenticada para o login
        e guarda o endereço que ela tentou abrir.
        """
        parametros = urlencode(
            {
                "next": request.get_full_path(),
            }
        )

        return redirect(
            f"{settings.LOGIN_URL}?{parametros}"
        )

    @staticmethod
    def informacoes_da_rota(request):
        """
        Descobre o namespace e o nome da página atual.
        """
        try:
            correspondencia = resolve(
                request.path_info
            )

        except Resolver404:
            return "", ""

        return (
            correspondencia.namespace or "",
            correspondencia.url_name or "",
        )

    def verificar_acesso(self, request):
        """
        Aplica as regras de acesso.
        """
        if self.caminho_publico(request):
            return None

        utilizador = request.user

        if not utilizador.is_authenticated:
            if request.path_info.startswith("/admin/"):
                return None

            return self.enviar_para_login(request)

        namespace, nome_rota = (
            self.informacoes_da_rota(request)
        )

        # O próprio Django controla o acesso ao painel admin.
        if request.path_info.startswith("/admin/"):
            if utilizador.is_staff:
                return None

            raise PermissionDenied(
                _(
                    "Não tem permissão para aceder "
                    "ao painel administrativo."
                )
            )

        # A página inicial é permitida porque encaminha
        # cada grupo para a área correta.
        if nome_rota == "home":
            return None

        # Superutilizadores e Administradores têm
        # acesso completo.
        if e_administrador(utilizador):
            return None

        # A Receção pode aceder às áreas operacionais.
        if e_recepcao(utilizador):
            namespaces_permitidos = {
                "clientes",
                "servicos",
                "funcionarios",
                "marcacoes",
                "mapa",
            }

            if namespace in namespaces_permitidos:
                return None

            raise PermissionDenied(
                _(
                    "Esta página está disponível apenas "
                    "para Administradores."
                )
            )

        # O Funcionário vê somente a própria agenda
        # e o próprio perfil.
        if e_funcionario(utilizador):
            rotas_permitidas = {
                "minha_agenda",
                "meu_perfil",
            }

            if (
                namespace == "utilizadores"
                and nome_rota in rotas_permitidas
            ):
                return None

            return redirect(
                "utilizadores:minha_agenda"
            )

        # Uma conta sem grupo não pode entrar nas
        # áreas internas da aplicação.
        raise PermissionDenied(
            _(
                "A sua conta ainda não possui um "
                "grupo de acesso autorizado."
            )
        )