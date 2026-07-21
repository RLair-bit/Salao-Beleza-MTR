# Sistema de Gestão de Salão de Beleza

Aplicação web para a receção de um salão de beleza gerir clientes, funcionários, serviços e marcações, com relatórios de atendimento.

![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0-092E20?logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8-4479A1?logo=mysql&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3?logo=bootstrap&logoColor=white)
![Estado](https://img.shields.io/badge/estado-em%20desenvolvimento-yellow)

---

## Índice

- [Sobre o projeto](#sobre-o-projeto)
- [Estado atual](#estado-atual)
- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Porquê estas tecnologias](#porquê-estas-tecnologias)
- [Pré-requisitos](#pré-requisitos)
- [Como executar](#como-executar)
- [Configuração da base de dados](#configuração-da-base-de-dados)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Roadmap](#roadmap)
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

## Estado atual

Já funcional:

- Projeto Django configurado e ligado a uma base de dados MySQL.
- **Modelos de dados** das quatro entidades principais: Cliente, Serviço, Funcionário e Marcação.
- **Área de administração** com todos os modelos registados, incluindo filtros, pesquisa e navegação por datas.
- **Regra de negócio das marcações** implementada e testada: o sistema recusa marcações sobrepostas para o mesmo funcionário e posto de trabalho com base na duração do serviço.
- **Estrutura base da interface** (template principal, barra de navegação e página inicial em Bootstrap).
- **Módulo de Marcações** funcional: agenda diária com filtro por data e formulário de nova marcação, fora da área de administração.
- **Postos de trabalho** (8 mesas/cadeiras), com validação que impede duas marcações na mesma mesa à mesma hora.

Em desenvolvimento: as páginas de gestão de clientes, serviços e funcionários, para que toda a gestão diária deixe de depender da área de administração.

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
| Linguagem | Python 3 |
| Framework | Django 6 |
| Base de dados | MySQL 8 (via PyMySQL) |
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
- [Git](https://git-scm.com/) ou [GitHub Desktop](https://desktop.github.com/)

---

## Como executar

```bash
# 1. Clonar o repositório
git clone https://github.com/RLair-bit/Salao-Beleza-MTR.git
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

# 4.1 Carregar os dados de exemplo (opcional)
python manage.py loaddata dados_exemplo.json

# 5. Criar um utilizador administrador
python manage.py createsuperuser

# 6. Arrancar o servidor de desenvolvimento
python manage.py runserver
```

A aplicação fica disponível em **http://127.0.0.1:8000** e a área de administração em **http://127.0.0.1:8000/admin**.

> A base de dados tem de ser criada previamente (ver secção seguinte). Cada elemento da equipa tem a sua própria base de dados local: o que se partilha neste repositório é o código, não os dados.

---

## Configuração da base de dados

No MySQL, criar a base de dados e o utilizador da aplicação:

```sql
CREATE DATABASE salao_beleza CHARACTER SET utf8mb4;
CREATE USER 'salao'@'localhost' IDENTIFIED BY 'salao2026';
GRANT ALL PRIVILEGES ON salao_beleza.* TO 'salao'@'localhost';
FLUSH PRIVILEGES;
```

Estas credenciais correspondem às que estão definidas em `salao/settings.py` e devem ser iguais em todas as máquinas da equipa, para que o ficheiro não tenha de ser alterado por cada pessoa.

> **Nota:** trata-se de uma base de dados local de desenvolvimento, sem dados reais. Numa fase posterior, as credenciais serão movidas para um ficheiro `.env` fora do repositório.

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
├── dados_exemplo.json  # Dados de teste partilhados pela equipa
├── requirements.txt
└── manage.py
```

---

## Roadmap

**Concluído**

- [x] Configuração do projeto e ligação ao MySQL
- [x] Modelos de dados (Cliente, Serviço, Funcionário, Marcação)
- [x] Área de administração
- [x] Validação de marcações sobrepostas
- [x] Estrutura base da interface
- [x] Agenda e formulário de Marcações
- [x] Postos de trabalho e validação de ocupação
- [x] Dados de exemplo partilhados

**Em curso**

- [ ] Páginas de Clientes (listar, criar, editar, pesquisar)
- [ ] Páginas de Serviços e Preçário
- [ ] Páginas de Funcionários
- [ ] Autenticação de utilizadores da receção
- [ ] Relatório de atendimentos
- [ ] Mapa do Salão

---

## Equipa

| Nome | Responsabilidades | GitHub |
|---|---|---|
| Rita | Marcações, estrutura base da interface e gestão do repositório | [@RLair-bit](https://github.com/RLair-bit) |
| Ticiana | Clientes, Serviços e Preçário, relatório de atendimentos | [@ticianacbd](https://github.com/ticianacbd) |
| Micaele | Funcionários, autenticação de utilizadores, mapa do salão | [@micanatahajlucas-ux](https://github.com/micanatahajlucas-ux) |

---

## Licença

Projeto desenvolvido para fins educativos no âmbito do curso do IEFP Setúbal.
