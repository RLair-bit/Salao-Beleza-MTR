from django.contrib.auth.models import Group, User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from clientes.forms import ClienteForm
from clientes.models import Cliente

# Create your tests here.


class AutenticadoMixin:
    """Cria uma conta de Receção e inicia sessão antes de cada teste."""

    def autenticar(self):
        utilizador = User.objects.create_user("rececao", password="teste12345")
        utilizador.groups.add(Group.objects.get(name="Receção"))
        self.client.login(username="rececao", password="teste12345")


# Testa o modelo Cliente
class ClienteModelTest(TestCase):

    def test_criar_cliente(self):
        cliente = Cliente.objects.create(
            nome="João Silva",
            telefone="912345678",
            email="joao@email.com"
        )

        self.assertEqual(cliente.nome, "João Silva")
        self.assertEqual(cliente.telefone, "912345678")

# Testa o formulário ClienteForm
class ClienteFormTest(TestCase):

    def test_formulario_valido(self):
        form = ClienteForm(data={
            "nome": "Maria",
            "telefone": "912345678",
            "email": "maria@email.com",
        })

        self.assertTrue(form.is_valid())

    def test_formulario_sem_nome(self):
        form = ClienteForm(data={
            "nome": "",
            "telefone": "912345678",
            "email": "maria@email.com",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("nome", form.errors)

# Testa as URLs e views relacionadas ao cliente
class ClienteUrlsTest(AutenticadoMixin, TestCase):

    def setUp(self):
        self.autenticar()

    def test_lista(self):
        response = self.client.get(reverse("clientes:listar"))
        self.assertEqual(response.status_code, 200)

# Testa as views de listagem e criação de clientes
class ClienteListViewTest(AutenticadoMixin, TestCase):

    def setUp(self):
        self.autenticar()
        Cliente.objects.create(
            nome="João",
            telefone="912345678",
            email="joao@email.com"
        )

    def test_lista_exibe_cliente(self):
        response = self.client.get(reverse("clientes:listar"))

        self.assertContains(response, "João")
        self.assertContains(response, "912345678")

    
    def test_pesquisa_cliente(self):

        Cliente.objects.create(
            nome="José Silva",
            telefone="111",
            email="jose@email.com"
        )

        Cliente.objects.create(
            nome="Maria Oliveira",
            telefone="222",
            email="maria@email.com"
        )

        response = self.client.get(
            reverse("clientes:listar"),
            {"q": "José"}
        )

        self.assertContains(response, "José Silva")
        self.assertNotContains(response, "Maria Oliveira")

# Testa a view de criação de clientes
class ClienteCreateViewTest(AutenticadoMixin, TestCase):

    def setUp(self):
        self.autenticar()

    def test_criar_cliente(self):

        response = self.client.post(
            reverse("clientes:criar"),
            {
                "nome": "Carlos",
                "telefone": "911111111",
                "email": "carlos@email.com",
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Cliente.objects.count(), 1)

# Testa a view de edição de clientes
class ClienteEditViewTest(AutenticadoMixin, TestCase):

    def setUp(self):
        self.autenticar()
        self.cliente = Cliente.objects.create(
            nome="João",
            telefone="912345678",
            email="joao@email.com"
        )

    def test_editar_cliente(self):

        response = self.client.post(
            reverse("clientes:editar", args=[self.cliente.pk]),
            {
                "nome": "João Pedro",
                "telefone": "999999999",
                "email": "jp@email.com",
            }
        )

        self.assertEqual(response.status_code, 302)

        self.cliente.refresh_from_db()

        self.assertEqual(self.cliente.nome, "João Pedro")

# Testa a view de exclusão de clientes
class ClienteDeleteViewTest(AutenticadoMixin, TestCase):

    def setUp(self):
        self.autenticar()
        self.cliente = Cliente.objects.create(
            nome="Maria",
            telefone="912345678",
            email="maria@email.com"
        )

    def test_excluir_cliente(self):

        response = self.client.post(
            reverse("clientes:excluir", args=[self.cliente.pk])
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Cliente.objects.filter(pk=self.cliente.pk).exists()
        )
