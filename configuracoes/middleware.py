from zoneinfo import ZoneInfo

from django.utils import timezone, translation

from .models import Configuracao


class ConfiguracaoMiddleware:
    """Aplica o idioma e o fuso horario definidos nas Configuracoes a cada pedido."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            config = Configuracao.obter()
            translation.activate(config.idioma)
            timezone.activate(ZoneInfo(config.fuso_horario))
        except Exception:
            pass                         # se a tabela ainda nao existir, usa os valores por omissao
        return self.get_response(request)