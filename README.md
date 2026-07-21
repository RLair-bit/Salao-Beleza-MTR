# Sistema de Gestão de Salão de Beleza

Aplicação web para a receção de um salão de beleza gerir clientes, funcionários, serviços e marcações, com relatórios de atendimento.

![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0-092E20?logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8-4479A1?logo=mysql&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3?logo=bootstrap&logoColor=white)
![Testes](https://img.shields.io/badge/testes-5%20a%20passar-16a34a)
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
- [Testes](#testes)
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

**Base do sistema**

- Projeto Django configurado e ligado a uma base de dados MySQL.
- Modelos de dados das cinco entidades: Cliente, Serviço, Funcionário, Marcação e Posto.
- Área de administração com todos os modelos registados, incluindo filtros, pesquisa e navegação por datas.
- Interface comum a toda a aplicação, com barra de navegação, mensagens de confirmação e tema visual próprio.

**Marcações**

- Agenda diária com navegação entre dias, filtro por funcionário e contagem de marcações.
- Criação e edição de marcações, com escolha de cliente, funcionário, serviço, mesa e horário.
- Alteração de estado a partir da agenda: realizada, faltou ou cancelada.
- **Regras de negócio implementadas e testadas:** o sistema recusa marcações sobrepostas para o mesmo funcionário e para a mesma mesa, com base na duração do serviço.
- Testes automáticos que verificam estas regras.

**Clientes**

- Registo, edição e listagem de clientes, com pesquisa por nome.
- Mensagens de confirmação nas operações efetuadas.

**Funcionários**

- Registo, edição e listagem de profissionais, com pesquisa e ordenação alfabética.
- Filtro por estado ativo ou inativo e associação aos serviços que cada profissional presta.
- Proteção contra eliminação de funcionários com marcações associadas.
- Página de detalhe com dados profissionais, serviços prestados, total de marcações e próximas marcações.

**Acesso ao sistema**

- Página de entrada com autenticação, saída de sessão e redirecionamento adequado em ambos os casos.
- Páginas protegidas, acessíveis apenas a utilizadores autenticados.

**Mapa do Salão**

- Vista das oito mesas do salão, com seleção da data a consultar.
- Identificação das mesas livres e ocupadas, com as respetivas marcações.
- Cartões de resumo com o total de mesas, mesas ocupadas, mesas livres e número de marcações do dia.

**Painel inicial**

- Página de entrada da aplicação com os indicadores do dia: marcações agendadas, já realizadas, receita e próximas marcações.

**Arranque em Windows**

- Ficheiro de atalho com ícone que ativa o ambiente, inicia o servidor e abre a aplicação no browser.

Em desenvolvimento: módulo de serviços e preçário, relatório de atendimentos e manual de utilização.

---

## Funcionalidades

- **Cadastro de Clientes** — nome, contacto, email e observações.
- **Cadastro de Funcionários** — profissionais do salão e os serviços que prestam.
- **Cadastro de Utilizadores** — contas de acesso à aplicação (receção e administração), com autenticação.
- **Serviços e Preçário** — serviços oferecidos, com preço e duração estimada.
- **Marcações** — agendar um serviço para um cliente, com funcionário, mesa, data e hora.
- **Mapa do Salão** — visualização dos postos de trabalho e respetiva ocupação.
- **Relatório de atendimentos** — resumo dos atendimentos realizados num período à escolha.

> **Regras de negócio principais:** o sistema impede que o mesmo funcionário seja marcado para dois clientes à mesma hora, e que a mesma mesa seja ocupada por duas marcações em simultâneo. Ambas têm em conta a duração definida para cada serviço.

---

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3 |
| Framework | Django 6 |
| Base de dados | MySQL 8 (via PyMySQL) |
| Interface | HTML + Bootstrap 5 e Bootstrap Icons |
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

> Em Windows, depois desta configuração inicial, a aplicação pode ser iniciada com um duplo clique no ficheiro `MTR-Gestão.bat`, que ativa o ambiente, arranca o servidor e abre o browser automaticamente.

> O acesso à aplicação exige autenticação. Utilizar a conta de administração criada no passo 5, ou outra criada a partir da área de administração.

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

## Testes

O projeto inclui testes automáticos que verificam as regras de negócio das marcações: aceitação de marcações válidas, recusa de sobreposições por funcionário e por mesa, aceitação de marcações consecutivas e libertação do horário quando uma marcação é cancelada.

Para os executar:

```bash
python manage.py test
```

O Django cria uma base de dados temporária, corre os testes e elimina-a no fim. É necessário dar previamente permissão ao utilizador da aplicação sobre essa base:

```sql
GRANT ALL PRIVILEGES ON `test\_salao\_beleza`.* TO 'salao'@'localhost';
FLUSH PRIVILEGES;
```

---

## Estrutura do projeto

```
Salao-Beleza-MTR/
├── salao/              # Configuração do projeto Django
│   ├── settings.py
│   └── urls.py
├── clientes/           # App: cadastro de clientes
├── funcionarios/       # App: cadastro de funcionários e autenticação
├── servicos/           # App: serviços e preçário
├── marcacoes/          # App: marcações e postos (módulo central)
├── mapa/               # App: mapa de ocupação das mesas
├── relatorios/         # App: relatório de atendimentos
├── templates/          # Templates HTML partilhados
├── dados_exemplo.json  # Dados de teste partilhados pela equipa
├── MTR-Gestão.bat      # Atalho de arranque para Windows
├── requirements.txt
└── manage.py
```

---

## Roadmap

**Concluído**

- [x] Configuração do projeto e ligação ao MySQL
- [x] Modelos de dados (Cliente, Serviço, Funcionário, Marcação, Posto)
- [x] Área de administração
- [x] Validação de marcações sobrepostas (funcionário e mesa)
- [x] Estrutura base da interface e identidade visual
- [x] Agenda, criação, edição e estados das Marcações
- [x] Navegação por dias e filtro por funcionário na agenda
- [x] Páginas de Clientes (listar, criar, editar, pesquisar)
- [x] Páginas de Funcionários, com detalhe e filtros
- [x] Autenticação de utilizadores e proteção das páginas
- [x] Mapa de ocupação das mesas
- [x] Painel inicial com indicadores do dia
- [x] Testes automáticos das regras de negócio
- [x] Dados de exemplo partilhados
- [x] Atalho de arranque com ícone
- [X] Páginas de Clientes

**Em curso**

- [ ] Páginas de Serviços e Preçário
- [ ] Relatório de atendimentos por período
- [ ] Eliminação de clientes
- [ ] Manual de utilização
- [ ] Preparação da apresentação final

---

## Equipa

| Nome | Responsabilidades | GitHub |
|---|---|---|
| Rita | Marcações, painel inicial, estrutura base da interface, testes e gestão do repositório | [@RLair-bit](https://github.com/RLair-bit) |
| Ticiana | Clientes, Serviços e Preçário, relatório de atendimentos | [@ticianacbd](https://github.com/ticianacbd) |
| Micaele | Funcionários, autenticação de utilizadores, mapa do salão | [@micanatahajlucas-ux](https://github.com/micanatahajlucas-ux) |

---

## Licença

Projeto desenvolvido para fins educativos no âmbito do curso do IEFP Setúbal.
