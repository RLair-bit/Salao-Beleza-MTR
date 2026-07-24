from django.shortcuts import render
from django.db.models import Count, Sum

from marcacoes.models import Marcacao
from relatorios.forms import RelatorioServicoForm

# Create your views here.
def relatorio_servicos(request):

    form = RelatorioServicoForm(request.GET or None)

    if form.is_valid():
        relatorio = Marcacao.objects.select_related("cliente")

        data_inicial = form.cleaned_data["data_inicial"]
        data_final = form.cleaned_data["data_final"]
        estados = form.cleaned_data["estados"]

        if data_inicial:
            relatorio = relatorio.filter(inicio__gte=data_inicial)

        if data_final:
            relatorio = relatorio.filter(inicio__lte=data_final)

        if estados:
            relatorio = relatorio.filter(estado__in=estados)

        total = relatorio.aggregate(
            total=Sum("servico__preco")
        )["total"] or 0

        relatorio = relatorio.order_by("inicio")
        return render(
            request,
            "servicos.html",
            {
                "form": form,
                "marcacoes": relatorio,
                "total": total,
            }
        )

    return render(
        request,
        "servicos.html",
        {
            "form": form,
            "marcacoes": None,
            "total": 0,
        }
    )
