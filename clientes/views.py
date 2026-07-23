from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.shortcuts import get_object_or_404, redirect, render

from clientes.forms import ClienteForm

from .models import Cliente


# Create your views here.
@login_required
def listar(request):
    q = request.GET.get("q", "")
    if q:
        clientes = Cliente.objects.filter(nome__icontains=q)
    else:
        clientes = Cliente.objects.all()

    return render(request, "clientes/lista.html", {"clientes": clientes, "procura": q})

@login_required
def criar(request):
    form = ClienteForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, _("Cliente criado com sucesso."))
        return redirect("clientes:listar")

    return render(request, "clientes/form.html", {"form": form, "titulo": _("Novo cliente")})

@login_required
def editar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    form = ClienteForm(request.POST or None, instance=cliente)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, _("Cliente atualizado com sucesso."))
        return redirect("clientes:listar")
    return render(request, "clientes/form.html", {"form": form, "cliente": cliente})

@login_required
def excluir(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == "POST":
        cliente.delete()
        messages.success(request, _("Cliente excluído com sucesso."))
        return redirect("clientes:listar")

    return render(request, "clientes/confirmar_exclusao.html", {"cliente": cliente})