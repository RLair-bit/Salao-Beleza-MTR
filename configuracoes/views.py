from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.shortcuts import redirect, render

from .forms import ConfiguracaoForm
from .models import Configuracao


@login_required
def editar(request):
    config = Configuracao.obter()
    form = ConfiguracaoForm(request.POST or None, instance=config)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, _("Configurações guardadas com sucesso."))
        return redirect("configuracoes:editar")
    return render(request, "configuracoes/editar.html", {"form": form})