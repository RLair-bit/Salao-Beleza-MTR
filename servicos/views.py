from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.shortcuts import get_object_or_404, redirect, render

from servicos.forms import ServicoForm
from servicos.models import Servico

# Create your views here.
@login_required
def listar(request):
    servicos = Servico.objects.all()
    return render(request, "servicos/lista.html", {"servicos": servicos})

@login_required
def criar(request):
    form = ServicoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, _("Serviço criado com sucesso."))
        return redirect("servicos:listar")

    return render(request, "servicos/form.html", {"form": form, "titulo": _("Novo serviço")})
    
@login_required
def editar(request, pk):
    servico = get_object_or_404(Servico, pk=pk)

    form = ServicoForm(request.POST or None, instance=servico)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, _("Serviço atualizado com sucesso."))
        return redirect("servicos:listar")
    return render(request, "servicos/form.html", {"form": form, "servico": servico})

@login_required
def excluir(request, pk):
    servico = get_object_or_404(Servico, pk=pk)

    if request.method == "POST":
        servico.delete()
        messages.success(request, _("Serviço excluído com sucesso."))
        return redirect("servicos:listar")

    return render(request, "servicos/confirmar_exclusao.html", {"servico": servico})