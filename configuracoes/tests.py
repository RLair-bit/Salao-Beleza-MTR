from datetime import datetime
from zoneinfo import ZoneInfo

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import formats, timezone

from .models import Configuracao


class ConfiguracaoModeloTest(TestCase):
    """Comportamento do registo unico (singleton)."""

    def test_valor_por_omissao(self):
        self.assertEqual(Configuracao.obter().nome_salao, "Salão de Beleza")

    def test_guardar_forca_sempre_o_mesmo_registo(self):
        c = Configuracao.obter()
        c.nome_salao = "Salão da Rita"
        c.save()
        Configuracao().save()
        self.assertEqual(Configuracao.objects.count(), 1)
        self.assertEqual(Configuracao.objects.get().pk, 1)

    def test_nao_se_apaga(self):
        Configuracao.obter().delete()
        self.assertEqual(Configuracao.objects.count(), 1)

    def test_idioma_e_fuso_por_omissao(self):
        c = Configuracao.obter()
        self.assertEqual(c.idioma, "pt-pt")
        self.assertEqual(c.fuso_horario, "Europe/Lisbon")


class AcessoConfiguracoesTest(TestCase):
    """Protecao por login e gravacao pela pagina."""

    def test_exige_login(self):
        r = self.client.get("/configuracoes/")
        self.assertEqual(r.status_code, 302)
        self.assertIn("/contas/login/", r["Location"])

    def test_acessivel_com_sessao(self):
        User.objects.create_user("dona", password="teste12345")
        self.client.login(username="dona", password="teste12345")
        self.assertEqual(self.client.get("/configuracoes/").status_code, 200)

    def test_guarda_alteracoes(self):
        User.objects.create_user("dona", password="teste12345")
        self.client.login(username="dona", password="teste12345")
        self.client.post("/configuracoes/", {
            "nome_salao": "Belo Cabelo",
            "hora_abertura": "09:00",
            "hora_fecho": "19:00",
            "idioma": "es",
            "fuso_horario": "America/Sao_Paulo",
        })
        c = Configuracao.obter()
        self.assertEqual(c.nome_salao, "Belo Cabelo")
        self.assertEqual(c.idioma, "es")

    def test_nome_do_salao_aparece_no_cabecalho(self):
        User.objects.create_user("dona", password="teste12345")
        self.client.login(username="dona", password="teste12345")
        c = Configuracao.obter()
        c.nome_salao = "Belo Cabelo"
        c.save()
        r = self.client.get("/")
        self.assertContains(r, "Belo Cabelo")


class IdiomaEFusoTest(TestCase):
    """O middleware aplica o idioma e o fuso escolhidos."""

    MOMENTO = datetime(2026, 7, 22, 12, 0, tzinfo=ZoneInfo("UTC"))

    def setUp(self):
        User.objects.create_user("dona", password="teste12345")
        self.client.login(username="dona", password="teste12345")

    def test_fuso_altera_a_hora_apresentada(self):
        c = Configuracao.obter()
        c.fuso_horario = "Asia/Tokyo"
        c.save()
        self.client.get("/")
        self.assertEqual(timezone.localtime(self.MOMENTO).strftime("%H:%M"), "21:00")

    def test_idioma_altera_nome_do_mes(self):
        c = Configuracao.obter()

        c.idioma = "en"
        c.save()
        self.client.get("/")
        self.assertEqual(str(formats.date_format(self.MOMENTO, "F")), "July")

        c.idioma = "fr"
        c.save()
        self.client.get("/")
        self.assertEqual(str(formats.date_format(self.MOMENTO, "F")), "juillet")

    def test_interface_traduzida(self):
        c = Configuracao.obter()
        c.idioma = "en"
        c.save()
        r = self.client.get("/marcacoes/")
        self.assertContains(r, "Appointments")
