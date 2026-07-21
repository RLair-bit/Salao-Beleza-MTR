from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import FuncionarioForm
from .models import Funcionario


def lista(request):
    procura = request.GET.get("q", "")
    funcionarios = Funcionario.objects.prefetch_related("servicos")

    if procura:
        funcionarios = funcionarios.filter(nome__icontains=procura)

    return render(
        request,
        "funcionarios/lista.html",
        {"funcionarios": funcionarios, "procura": procura},
    )


def criar(request):
    form = FuncionarioForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Funcionário criado com sucesso.")
        return redirect("funcionarios:lista")

    return render(
        request,
        "funcionarios/form.html",
        {"form": form, "titulo": "Novo funcionário"},
    )


def editar(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    form = FuncionarioForm(request.POST or None, instance=funcionario)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Funcionário atualizado.")
        return redirect("funcionarios:lista")

    return render(
        request,
        "funcionarios/form.html",
        {"form": form, "titulo": f"Editar {funcionario.nome}"},
    )


def eliminar(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)

    if request.method == "POST":
        try:
            funcionario.delete()
            messages.success(request, "Funcionário eliminado.")
        except Exception:
            messages.error(
                request,
                "Não é possível eliminar: este funcionário tem marcações associadas. "
                "Em alternativa, desativa-o.",
            )

        return redirect("funcionarios:lista")

    return render(
        request,
        "funcionarios/confirmar_eliminar.html",
        {"funcionario": funcionario},
    )