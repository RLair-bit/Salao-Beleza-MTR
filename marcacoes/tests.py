from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from clientes.models import Cliente
from funcionarios.models import Funcionario
from servicos.models import Servico

from .models import Marcacao, Posto


class ValidacaoMarcacoesTest(TestCase):
    def setUp(self):
        self.servico = Servico.objects.create(nome="Corte", preco=15, duracao_min=30)
        self.ana = Funcionario.objects.create(nome="Ana Silva")
        self.bruno = Funcionario.objects.create(nome="Bruno Costa")
        self.c1 = Cliente.objects.create(nome="Cliente Um", telefone="910000001")
        self.c2 = Cliente.objects.create(nome="Cliente Dois", telefone="910000002")
        self.mesa1 = Posto.objects.create(numero=1)
        self.mesa2 = Posto.objects.create(numero=2)
        self.hora = timezone.now().replace(hour=10, minute=0, second=0, microsecond=0)

    def marcar(self, cliente, funcionario, posto, minutos=0):
        return Marcacao.objects.create(
            cliente=cliente,
            funcionario=funcionario,
            servico=self.servico,
            posto=posto,
            inicio=self.hora + timedelta(minutes=minutos),
        )

    def test_marcacao_simples_e_aceite(self):
        self.marcar(self.c1, self.ana, self.mesa1)
        self.assertEqual(Marcacao.objects.count(), 1)

    def test_recusa_funcionario_com_horario_sobreposto(self):
        self.marcar(self.c1, self.ana, self.mesa1)
        with self.assertRaises(ValidationError):
            self.marcar(self.c2, self.ana, self.mesa2, minutos=15)

    def test_recusa_mesa_ja_ocupada(self):
        self.marcar(self.c1, self.ana, self.mesa1)
        with self.assertRaises(ValidationError):
            self.marcar(self.c2, self.bruno, self.mesa1, minutos=15)

    def test_aceita_marcacao_seguida(self):
        self.marcar(self.c1, self.ana, self.mesa1)
        self.marcar(self.c2, self.ana, self.mesa1, minutos=30)
        self.assertEqual(Marcacao.objects.count(), 2)

    def test_marcacao_cancelada_nao_bloqueia_horario(self):
        m = self.marcar(self.c1, self.ana, self.mesa1)
        m.estado = "cancelada"
        m.save()
        self.marcar(self.c2, self.ana, self.mesa1, minutos=15)
        self.assertEqual(Marcacao.objects.filter(estado="marcada").count(), 1)