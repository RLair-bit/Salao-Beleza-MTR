from django.contrib import messages

from django.shortcuts import redirect, render

from clientes.forms import ClienteForm

from .models import Cliente


# Create your views here.
def listar(request):
    q = request.GET.get("q", "")
    if q:
        clientes = Cliente.objects.filter(nome__icontains=q)
    else:
        clientes = Cliente.objects.all()

    return render(request, "clientes/lista.html", {"clientes": clientes, "procura": q})


def criar(request):
    form = ClienteForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Cliente criado com sucesso.")
        return redirect("clientes:listar")

    return render(request, "clientes/form.html", {"form": form, "titulo": "Novo cliente"})


def editar(request, pk):
    cliente = Cliente.objects.get(pk=pk)
    if not cliente:
        messages.error(request, "Cliente não encontrado.")
        return redirect("clientes:listar")

    form = ClienteForm(request.POST or None, instance=cliente)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Cliente atualizado com sucesso.")
        return redirect("clientes:listar")
    return render(request, "clientes/form.html", {"form": form, "cliente": cliente})
