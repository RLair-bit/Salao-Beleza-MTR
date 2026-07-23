from datetime import datetime, time

from django.conf import settings
from django.utils import timezone

from .models import Marcacao


def pendentes_antigas(request):
    """
    Conta as marcações de dias anteriores que continuam no
    estado "marcada", ou seja, que ficaram por fechar.
    """
    if not request.user.is_authenticated:
        return {"n_pendentes_antigas": 0}

    inicio_hoje = datetime.combine(timezone.localdate(), time.min)

    if settings.USE_TZ:
        inicio_hoje = timezone.make_aware(
            inicio_hoje,
            timezone.get_current_timezone(),
        )

    total = Marcacao.objects.filter(
        estado="marcada",
        inicio__lt=inicio_hoje,
    ).count()

    return {"n_pendentes_antigas": total}
