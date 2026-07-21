from datetime import datetime, time, timedelta

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from marcacoes.models import Marcacao, Posto


@login_required
def mapa(request):
    try:
        dia = datetime.strptime(request.GET["dia"], "%Y-%m-%d").date()
    except (KeyError, ValueError):
        dia = timezone.localdate()

    inicio = datetime.combine(dia, time.min)
    fim = inicio + timedelta(days=1)

    if settings.USE_TZ:
        inicio = timezone.make_aware(inicio)
        fim = timezone.make_aware(fim)

    marcacoes = (
        Marcacao.objects
        .filter(inicio__gte=inicio, inicio__lt=fim)
        .exclude(estado="cancelada")
        .select_related("cliente", "funcionario", "servico", "posto")
    )

    mesas = []

    for posto in Posto.objects.all():
        do_posto = [m for m in marcacoes if m.posto_id == posto.id]
        mesas.append({
            "posto": posto,
            "marcacoes": do_posto,
        })

    total_mesas = len(mesas)
    mesas_ocupadas = sum(1 for m in mesas if m["marcacoes"])
    mesas_livres = total_mesas - mesas_ocupadas
    total_marcacoes = sum(len(m["marcacoes"]) for m in mesas)

    return render(
        request,
        "mapa/mapa.html",
        {
            "dia": dia,
            "mesas": mesas,
            "total_mesas": total_mesas,
            "mesas_ocupadas": mesas_ocupadas,
            "mesas_livres": mesas_livres,
            "total_marcacoes": total_marcacoes,
        },
    )