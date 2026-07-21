from django.shortcuts import redirect, render

from clientes.forms import ClienteForm

from .models import Cliente


# Create your views here.
def listar(request):
    clientes = Cliente.objects.all()
    context = {
        'clientes': clientes,
    }
    return render(request, 'clientes/lista.html', context)

def criar(request):
    form = ClienteForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('clientes:lista')
    return render(request, 'clientes/criar.html', {'form': form})

def editar(request, pk):
    cliente = Cliente.objects.get(pk=pk)
    form = ClienteForm(request.POST or None, instance=cliente)
    if form.is_valid():
        form.save()
        return redirect('clientes:lista')
    return render(request, 'clientes/editar.html', {'form': form, 'cliente': cliente})