from datetime import timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from clientes.models import Cliente
from funcionarios.models import Funcionario
from servicos.models import Servico

from .models import Marcacao, Posto


class ValidacaoMarcacoesTest(TestCase):
    """Regras de negocio: sobreposicoes de funcionario e de mesa."""

    def setUp(self):
        self.servico = Servico.objects.create(
            nome="Corte", preco=15, duracao_min=30,
        )
        self.ana = Funcionario.objects.create(nome="Ana Silva")
        self.bruno = Funcionario.objects.create(nome="Bruno Costa")
        self.c1 = Cliente.objects.create(nome="Cliente Um", telefone="910000001")
        self.c2 = Cliente.objects.create(nome="Cliente Dois", telefone="910000002")
        self.mesa1 = Posto.objects.create(numero=1)
        self.mesa2 = Posto.objects.create(numero=2)
        self.hora = timezone.now().replace(
            hour=10, minute=0, second=0, microsecond=0,
        )

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

    def test_funcionarios_diferentes_em_mesas_diferentes(self):
        self.marcar(self.c1, self.ana, self.mesa1)
        self.marcar(self.c2, self.bruno, self.mesa2, minutos=45)
        self.assertEqual(Marcacao.objects.count(), 2)

    def test_edicao_nao_colide_consigo_mesma(self):
        m = self.marcar(self.c1, self.ana, self.mesa1)
        m.notas = "alterada"
        m.save()
        self.assertEqual(Marcacao.objects.count(), 1)


class PropriedadesMarcacaoTest(TestCase):
    """Propriedades derivadas: fim, a_decorrer e em_atraso."""

    def setUp(self):
        self.servico = Servico.objects.create(
            nome="Coloracao", preco=40, duracao_min=60,
        )
        self.ana = Funcionario.objects.create(nome="Ana Silva")
        self.cliente = Cliente.objects.create(nome="Cliente", telefone="910000003")
        self.mesa = Posto.objects.create(numero=1)

    def nova(self, inicio, estado="marcada"):
        return Marcacao.objects.create(
            cliente=self.cliente,
            funcionario=self.ana,
            servico=self.servico,
            posto=self.mesa,
            inicio=inicio,
            estado=estado,
        )

    def test_fim_soma_duracao_do_servico(self):
        inicio = timezone.now() + timedelta(days=1)
        m = self.nova(inicio)
        self.assertEqual(m.fim, inicio + timedelta(minutes=60))

    def test_em_atraso_quando_ja_passou(self):
        m = self.nova(timezone.now() - timedelta(hours=2))
        self.assertTrue(m.em_atraso)
        self.assertFalse(m.a_decorrer)

    def test_a_decorrer_dentro_da_duracao(self):
        m = self.nova(timezone.now() - timedelta(minutes=10))
        self.assertTrue(m.a_decorrer)
        self.assertFalse(m.em_atraso)

    def test_marcacao_futura_nao_esta_em_atraso(self):
        m = self.nova(timezone.now() + timedelta(hours=3))
        self.assertFalse(m.em_atraso)
        self.assertFalse(m.a_decorrer)

    def test_realizada_nunca_esta_em_atraso(self):
        m = self.nova(timezone.now() - timedelta(hours=2), estado="realizada")
        self.assertFalse(m.em_atraso)
        self.assertFalse(m.a_decorrer)


class AcessoMarcacoesTest(TestCase):
    """Protecao por login das paginas de marcacoes."""

    def test_agenda_exige_login(self):
        r = self.client.get("/marcacoes/")
        self.assertEqual(r.status_code, 302)
        self.assertIn("/contas/login/", r["Location"])

    def test_pendentes_exige_login(self):
        r = self.client.get("/marcacoes/pendentes/")
        self.assertEqual(r.status_code, 302)

    def test_paginas_abrem_com_sessao(self):
        User.objects.create_user("rececao", password="teste12345")
        self.client.login(username="rececao", password="teste12345")
        self.assertEqual(self.client.get("/marcacoes/").status_code, 200)
        self.assertEqual(self.client.get("/marcacoes/pendentes/").status_code, 200)


class PendentesAntigasTest(TestCase):
    """Marcacoes de dias anteriores que ficaram por fechar."""

    def setUp(self):
        self.servico = Servico.objects.create(
            nome="Corte", preco=15, duracao_min=30,
        )
        self.ana = Funcionario.objects.create(nome="Ana Silva")
        self.cliente = Cliente.objects.create(nome="Cliente", telefone="910000004")
        self.mesa = Posto.objects.create(numero=1)
        User.objects.create_user("rececao", password="teste12345")
        self.client.login(username="rececao", password="teste12345")

    def nova(self, dias, estado="marcada"):
        m = Marcacao.objects.create(
            cliente=self.cliente,
            funcionario=self.ana,
            servico=self.servico,
            posto=self.mesa,
            inicio=timezone.now() - timedelta(days=dias),
        )
        if estado != "marcada":
            m.estado = estado
            m.save()
        return m

    def test_conta_marcacoes_por_fechar_de_dias_anteriores(self):
        self.nova(dias=2)
        self.nova(dias=5)
        r = self.client.get("/")
        self.assertEqual(r.context["n_pendentes_antigas"], 2)

    def test_marcacao_de_hoje_nao_conta(self):
        Marcacao.objects.create(
            cliente=self.cliente,
            funcionario=self.ana,
            servico=self.servico,
            posto=self.mesa,
            inicio=timezone.now() + timedelta(hours=2),
        )
        r = self.client.get("/")
        self.assertEqual(r.context["n_pendentes_antigas"], 0)

    def test_marcacao_antiga_ja_resolvida_nao_conta(self):
        self.nova(dias=3, estado="realizada")
        r = self.client.get("/")
        self.assertEqual(r.context["n_pendentes_antigas"], 0)

    def test_pagina_lista_as_pendentes(self):
        self.nova(dias=2)
        r = self.client.get("/marcacoes/pendentes/")
        self.assertEqual(r.context["total"], 1)

    def test_anonimo_nao_recebe_contagem(self):
        self.client.logout()
        r = self.client.get("/contas/login/")
        self.assertEqual(r.context["n_pendentes_antigas"], 0)


class PaginacaoTest(TestCase):
    """A agenda pagina quando ha muitas marcacoes."""

    def setUp(self):
        self.servico = Servico.objects.create(
            nome="Corte", preco=15, duracao_min=30,
        )
        self.cliente = Cliente.objects.create(nome="Cliente", telefone="910000005")
        User.objects.create_user("rececao", password="teste12345")
        self.client.login(username="rececao", password="teste12345")

        # 25 marcacoes no mesmo dia, cada uma com funcionario e mesa proprios
        base = timezone.now().replace(hour=9, minute=0, second=0, microsecond=0)
        for i in range(25):
            Marcacao.objects.create(
                cliente=self.cliente,
                funcionario=Funcionario.objects.create(nome=f"Func {i}"),
                servico=self.servico,
                posto=Posto.objects.create(numero=i + 1),
                inicio=base,
            )

    def test_primeira_pagina_traz_20(self):
        r = self.client.get("/marcacoes/")
        self.assertEqual(len(r.context["marcacoes"]), 20)

    def test_segunda_pagina_traz_o_resto(self):
        dia = timezone.localdate().strftime("%Y-%m-%d")
        r = self.client.get(f"/marcacoes/?dia={dia}&pagina=2")
        self.assertEqual(len(r.context["marcacoes"]), 5)

    def test_total_mostra_todas_e_nao_so_a_pagina(self):
        r = self.client.get("/marcacoes/")
        self.assertEqual(r.context["total"], 25)

    def test_pagina_invalida_devolve_a_ultima(self):
        r = self.client.get("/marcacoes/?pagina=999")
        self.assertEqual(r.context["pagina"].number, 2)
