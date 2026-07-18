# 💇 Sistema de Gestão de Salão de Beleza

> Aplicação web para a **receção de um salão de beleza** gerir clientes, funcionários, serviços e marcações, com relatórios de atendimento.

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5-092E20?logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8-4479A1?logo=mysql&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3?logo=bootstrap&logoColor=white)
![Estado](https://img.shields.io/badge/estado-em%20desenvolvimento-yellow)

---

## 📑 Índice

- [Sobre o projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias](#-tecnologias)
- [Pré-requisitos](#-pré-requisitos)
- [Como executar](#-como-executar)
- [Configuração da base de dados](#-configuração-da-base-de-dados)
- [Estrutura do projeto](#-estrutura-do-projeto)
- [Estado e roadmap](#-estado-e-roadmap)
- [Equipa](#-equipa)
- [Licença](#-licença)

---

## 📋 Sobre o projeto

Projeto final desenvolvido no âmbito do curso **Técnico/a de Informática — Instalação e Gestão de Redes** (IEFP Setúbal), por uma equipa de 3 pessoas.

O objetivo é criar uma aplicação de **gestão de salão de beleza**, pensada para ser usada na **receção**: registar clientes e funcionários, definir os serviços e o preçário, e sobretudo **gerir as marcações** do dia a dia.

- **Público-alvo:** receção do salão
- **Módulo central:** Marcações
- **Formador:** `[preencher]`

---

## ✨ Funcionalidades

- **Cadastro de Clientes** — dados de contacto e histórico.
- **Cadastro de Funcionários** — profissionais do salão e os serviços que prestam.
- **Cadastro de Utilizadores** — contas de acesso à aplicação (receção / administração), com autenticação.
- **Serviços e Preçário** — lista de serviços oferecidos e respetivos preços e duração.
- **Marcações** — agendar um serviço para um cliente com um funcionário, numa data e hora.
- **Mapa do Salão** — visão das estações/postos e a sua ocupação.
- **Relatório de atendimentos** — resumo dos atendimentos num período à escolha.

---

## 🛠️ Tecnologias

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.12 |
| Framework | Django 5 |
| Base de dados | MySQL 8 (ou PostgreSQL) |
| Front-end | HTML, Bootstrap 5 |
| Controlo de versões | Git + GitHub |

---

## ✅ Pré-requisitos

Antes de começar, é preciso ter instalado:

- [Python 3.10+](https://www.python.org/)
- [MySQL 8](https://dev.mysql.com/downloads/) (ou PostgreSQL)
- [Git](https://git-scm.com/)

---

## 🚀 Como executar

```bash
# 1. Clonar o repositório
git clone [URL-DO-REPOSITORIO]
cd salao-beleza

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

> **Nota:** se ainda não existir um `requirements.txt`, gerem um com `pip freeze > requirements.txt` depois de instalarem o Django (`pip install django mysqlclient`).

---

## 🗄️ Configuração da base de dados

Criar a base de dados no MySQL:

```sql
CREATE DATABASE salao_beleza CHARACTER SET utf8mb4;
```

E configurar em `salao/settings.py`:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "salao_beleza",
        "USER": "[o_teu_utilizador]",
        "PASSWORD": "[a_tua_password]",
        "HOST": "127.0.0.1",
        "PORT": "3306",
    }
}
```

> Para **PostgreSQL**, trocar o `ENGINE` para `django.db.backends.postgresql`, a porta para `5432` e instalar `psycopg2-binary` em vez de `mysqlclient`.

---

## 📁 Estrutura do projeto

```
salao-beleza/
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

## 🗺️ Estado e roadmap

Prioridade para a **primeira demo**: fluxo de marcações a funcionar (criar marcação → ver na lista).

- [ ] Cadastro de Clientes
- [ ] Cadastro de Funcionários
- [ ] Serviços e Preçário
- [ ] **Marcações** *(módulo central — MVP)*
- [ ] Cadastro de Utilizadores / autenticação
- [ ] Relatório de atendimentos
- [ ] Mapa do Salão

---

## 👥 Equipa

| Nome | Responsabilidades | GitHub |
|---|---|---|
| `[Nome 1]` | `[ex.: modelos e base de dados]` | `[@user]` |
| `[Nome 2]` | `[ex.: marcações e views]` | `[@user]` |
| `[Nome 3]` | `[ex.: front-end e relatórios]` | `[@user]` |

---

## 📄 Licença

Projeto desenvolvido para fins **educativos** no âmbito do curso do IEFP Setúbal.
