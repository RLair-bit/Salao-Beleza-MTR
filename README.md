# Sistema de Gestão de Salão de Beleza

Aplicação web para a receção de um salão de beleza gerir clientes, funcionários, serviços e marcações, com relatórios de atendimento.

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5-092E20?logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8-4479A1?logo=mysql&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3?logo=bootstrap&logoColor=white)
![Estado](https://img.shields.io/badge/estado-em%20desenvolvimento-yellow)

---

## Índice

- [Sobre o projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Porquê estas tecnologias](#porquê-estas-tecnologias)
- [Pré-requisitos](#pré-requisitos)
- [Como executar](#como-executar)
- [Configuração da base de dados](#configuração-da-base-de-dados)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Estado e roadmap](#estado-e-roadmap)
- [Equipa](#equipa)
- [Licença](#licença)

---

## Sobre o projeto

Projeto final desenvolvido no âmbito do curso **Técnico/a de Informática — Instalação e Gestão de Redes** (Centro de Formação Profissional de Setúbal, IEFP), por uma equipa de três elementos.

O objetivo é criar uma aplicação de **gestão de salão de beleza**, pensada para ser usada na **receção**: registar clientes e funcionários, definir os serviços e o preçário, e sobretudo **gerir as marcações** do dia a dia.

- **Público-alvo:** receção do salão (rececionista e responsável)
- **Módulo central:** Marcações
- **Formador:** Tiago Dias

---

## Funcionalidades

- **Cadastro de Clientes** — nome, contacto, email e observações.
- **Cadastro de Funcionários** — profissionais do salão e os serviços que prestam.
- **Cadastro de Utilizadores** — contas de acesso à aplicação (receção e administração), com autenticação.
- **Serviços e Preçário** — serviços oferecidos, com preço e duração estimada.
- **Marcações** — agendar um serviço para um cliente com um funcionário, numa data e hora.
- **Mapa do Salão** — visualização dos postos de trabalho e respetiva ocupação.
- **Relatório de atendimentos** — resumo dos atendimentos realizados num período à escolha.

> **Regra de negócio principal:** o sistema impede que o mesmo funcionário seja marcado para dois clientes à mesma hora, tendo em conta a duração definida para cada serviço.

---

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.12 |
| Framework | Django 5 |
| Base de dados | MySQL 8 |
| Interface | HTML + Bootstrap 5 |
| Controlo de versões | Git + GitHub |

---

## Porquê estas tecnologias

| Opção adotada | Alternativas ponderadas | Razão da escolha |
|---|---|---|
| Django (Python) | NestJS/TypeScript, PHP, Laravel | O projeto assenta em formulários, tabelas e dados relacionados — o que o Django resolve de origem, com ORM, autenticação e área de administração automática. |
| MySQL | PostgreSQL, MongoDB, SQLite | Os dados são relacionais: uma marcação depende de um cliente, de um funcionário e de um serviço. Uma base não relacional obrigaria a garantir essa integridade por código. |
| Bootstrap 5 | Tailwind CSS, CSS de raiz | Componentes prontos e comportamento responsivo sem configuração adicional, poupando tempo em aspetos visuais. |
| Páginas geradas no servidor | Aplicação em React com API separada | Sendo uma aplicação interna, sem atualização em tempo real, os templates do Django dispensam a manutenção de dois projetos distintos. |
| Git + GitHub | Partilha por pen, email ou Drive | Permite trabalho em simultâneo sem sobreposição de ficheiros e mantém o histórico de alterações. |

---

## Pré-requisitos

- [Python 3.10+](https://www.python.org/)
- [MySQL 8](https://dev.mysql.com/downloads/)
- [Git](https://git-scm.com/)

---

## Como executar

```bash
# 1. Clonar o repositório
git clone https://github.com/[o-teu-user]/Salao-Beleza-MTR.git
cd Salao-Beleza-MTR

# 2. Criar e ativar o ambiente virtual
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux / macOS:
source venv/bin/activate

# 3. Instalar as dependências
pip install -r requirements.txt

# 4. Aplicar as migrações à base de dados
python manage.py migrate

# 5. Criar um utilizador administrador
python manage.py createsuperuser

# 6. Arrancar o servidor de desenvolvimento
python manage.py runserver
```

A aplicação fica disponível em **http://localhost:8000** e a área de administração em **http://localhost:8000/admin**.

> Se ainda não existir um `requirements.txt`, gerar um com `pip freeze > requirements.txt` depois de instalar as dependências (`pip install django mysqlclient`).

---

## Configuração da base de dados

Criar a base de dados no MySQL:

```sql
CREATE DATABASE salao_beleza CHARACTER SET utf8mb4;
```

Configurar em `salao/settings.py`:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "salao_beleza",
        "USER": "[utilizador]",
        "PASSWORD": "[password]",
        "HOST": "127.0.0.1",
        "PORT": "3306",
    }
}
```

> **Importante:** as credenciais não devem ser enviadas para o repositório. Guardar num ficheiro `.env` local, já ignorado pelo `.gitignore`.

---

## Estrutura do projeto

```
Salao-Beleza-MTR/
├── salao/              # Configuração do projeto Django
│   ├── settings.py
│   └── urls.py
├── clientes/           # App: cadastro de clientes
├── funcionarios/       # App: cadastro de funcionários
├── servicos/           # App: serviços e preçário
├── marcacoes/          # App: marcações (módulo central)
├── relatorios/         # App: relatório de atendimentos
├── templates/          # Templates HTML partilhados
├── static/             # CSS, imagens, JS
├── requirements.txt
└── manage.py
```

---

## Estado e roadmap

Prioridade inicial: fluxo de marcações a funcionar de ponta a ponta (criar marcação, ver na lista).

- [ ] Cadastro de Clientes
- [ ] Serviços e Preçário
- [ ] Cadastro de Funcionários
- [ ] **Marcações** (módulo central)
- [ ] Cadastro de Utilizadores e autenticação
- [ ] Relatório de atendimentos
- [ ] Mapa do Salão

---

## Equipa

| Nome | Responsabilidades | GitHub |
|---|---|---|
| Ticiana | [a definir — ex.: modelos e base de dados] | [@user] |
| Micaele | [a definir — ex.: módulo de marcações] | [@user] |
| Rita | Gestão do repositório GitHub (por enquanto); [restante a definir] | [@user] |

---

## Licença

Projeto desenvolvido para fins educativos no âmbito do curso do IEFP Setúbal.
