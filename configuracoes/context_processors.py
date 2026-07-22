from .models import Configuracao


def configuracao(request):
    """Disponibiliza {{ config }} em todos os templates."""
    try:
        return {"config": Configuracao.obter()}
    except Exception:
        return {"config": None}          # se a migracao ainda nao correu