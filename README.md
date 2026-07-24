# Sistema de Gestão de Salão de Beleza

Aplicação web para a receção de um salão de beleza gerir clientes, funcionários, serviços e marcações, com controlo de acesso por perfis e interface multilingue.

![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0-092E20?logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8-4479A1?logo=mysql&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3?logo=bootstrap&logoColor=white)
![Idiomas](https://img.shields.io/badge/idiomas-PT%20|%20ES%20|%20EN%20|%20FR-0ea5e9)
![Testes](https://img.shields.io/badge/testes-44%20a%20passar-16a34a)
![Estado](https://img.shields.io/badge/estado-em%20desenvolvimento-yellow)

---

## Índice

- [Sobre o projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Perfis de acesso](#perfis-de-acesso)
- [Idiomas e fuso horário](#idiomas-e-fuso-horário)
- [Tecnologias](#tecnologias)
- [Porquê estas tecnologias](#porquê-estas-tecnologias)
- [Pré-requisitos](#pré-requisitos)
- [Como executar](#como-executar)
- [Configuração da base de dados](#configuração-da-base-de-dados)
- [Testes](#testes)
- [Traduções](#traduções)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Convenções da equipa](#convenções-da-equipa)
- [Roadmap](#roadmap)
- [Limitações conhecidas](#limitações-conhecidas)
- [Equipa](#equipa)
- [Licença](#licença)

---

## Sobre o projeto

Projeto final desenvolvido no âmbito do curso **Técnico/a de Informática — Instalação e Gestão de Redes** (Centro de Formação Profissional de Setúbal, IEFP), por uma equipa de três elementos.

O objetivo é criar uma aplicação de **gestão de salão de beleza**, pensada para ser usada na **receção**: registar clientes e funcionários, definir os serviços e o preçário, e sobretudo **gerir as marcações** do dia a dia.

- **Público-alvo:** receção do salão, responsável e profissionais
- **Módulo central:** Marcações
- **Formador:** Tiago Dias

---

## Funcionalidades

### Marcações

Agenda diária com navegação entre dias e filtro por funcionário. Criação e edição de marcações com escolha de cliente, funcionário, serviço, mesa e horário, e alteração de estado a partir da agenda (realizada, faltou, cancelada).

Ao criar uma marcação, o sistema **calcula e apresenta os horários disponíveis**, tendo em conta a duração do serviço e as marcações já existentes.

> **Regras de negócio principais:** o sistema impede que o mesmo funcionário seja marcado para dois clientes à mesma hora, e que a mesma mesa seja ocupada por duas marcações em simultâneo. Ambas têm em conta a duração definida para cada serviço. Marcações canceladas não bloqueiam o horário.

O painel inicial assinala as marcações **em atraso** (já passaram da hora e continuam por fechar) e as que estão **a decorrer**. Existe ainda um aviso para marcações de **dias anteriores** que ficaram por resolver, com página própria para as fechar rapidamente.

### Clientes

Registo, edição e listagem com pesquisa por nome. Eliminação com página de confirmação e proteção contra a remoção de clientes que tenham marcações associadas.

### Funcionários

Registo, edição, listagem e página de detalhe dos profissionais, com pesquisa, filtro por estado e ordenação alfabética. Cada funcionário tem **horários de trabalho** e **ausências** configuráveis (folgas, férias, doença), fotografia e associação aos serviços que presta. Proteção contra eliminação de funcionários com marcações associadas.

### Serviços e Preçário

Catálogo de serviços com nome, preço, duração e estado ativo/inativo. A duração definida aqui alimenta o cálculo de conflitos nas marcações.

### Utilizadores e acesso

Gestão de contas com **três perfis de acesso** (ver secção seguinte), alteração da própria palavra-passe e área pessoal para os profissionais, onde cada um consulta a sua agenda, o seu horário de trabalho e o resumo do dia — incluindo o total faturado nos atendimentos concluídos.

### Relatórios

Relatório de serviços por período, com apuramento dos respetivos totais.

### Mapa do Salão

Vista das oito mesas do salão, com seleção da data a consultar, identificação das mesas livres e ocupadas, e cartões de resumo com os totais do dia.

### Definições do Salão

Aba onde o responsável configura o nome do salão, contactos, morada, horário de funcionamento, idioma e fuso horário. O nome escolhido reflete-se em toda a aplicação.

---

## Perfis de acesso

O acesso às páginas é controlado por grupos, através de um middleware próprio.

| Perfil | Acesso |
|---|---|
| **Administrador** | Acesso completo, incluindo definições do salão e gestão de contas de utilizador |
| **Receção** | Áreas operacionais: marcações, clientes, serviços, funcionários, mapa do salão e relatórios |
| **Funcionário** | Apenas a própria agenda, o próprio horário e o próprio perfil |

Os grupos são criados automaticamente por uma migração, ficando disponíveis em todas as instalações sem configuração manual.

---

## Idiomas e fuso horário

A aplicação funciona em **quatro idiomas** — Português (Portugal), Español, English e Français — configuráveis na aba de Definições, sem alterar código. Estão traduzidas **353 frases** por idioma.

O **fuso horário** é igualmente configurável, com opções agrupadas por continente (Europa, África, América, Ásia e Oceânia).

A tradução assenta no sistema de internacionalização (i18n) do Django: as frases são marcadas nos templates com `{% trans %}` e `{% blocktrans %}` e no Python com `gettext`, e as traduções ficam nos catálogos da pasta `locale/`.

---

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3 |
| Framework | Django 6 |
| Base de dados | MySQL 8 (via PyMySQL) |
| Interface | HTML + Bootstrap 5 e Bootstrap Icons |
| Imagens | Pillow |
| Internacionalização | Django i18n + GNU gettext |
| Controlo de versões | Git + GitHub |

---

## Porquê estas tecnologias

| Opção adotada | Alternativas ponderadas | Razão da escolha |
|---|---|---|
| Django (Python) | NestJS/TypeScript, PHP, Laravel | O projeto assenta em formulários, tabelas e dados relacionados — o que o Django resolve de origem, com ORM, autenticação, área de administração automática e suporte de internacionalização. |
| MySQL | PostgreSQL, MongoDB, SQLite | Os dados são relacionais: uma marcação depende de um cliente, de um funcionário e de um serviço. Uma base não relacional obrigaria a garantir essa integridade por código. |
| Bootstrap 5 | Tailwind CSS, CSS de raiz | Componentes prontos e comportamento responsivo sem configuração adicional, poupando tempo em aspetos visuais. |
| Páginas geradas no servidor | Aplicação em React com API separada | Sendo uma aplicação interna, sem atualização em tempo real, os templates do Django dispensam a manutenção de dois projetos distintos. |
| Git + GitHub | Partilha por pen, email ou Drive | Permite trabalho em simultâneo sem sobreposição de ficheiros e mantém o histórico de alterações. |

---

## Pré-requisitos

- [Python 3.12+](https://www.python.org/) (desenvolvido em 3.14)
- [MySQL 8](https://dev.mysql.com/downloads/)
- [Git](https://git-scm.com/) ou [GitHub Desktop](https://desktop.github.com/)
- [GNU gettext para Windows](https://mlocati.github.io/articles/gettext-iconv-windows.html) — apenas para gerar ou recompilar traduções

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

# 4. Aplicar as migrações (cria também os grupos de acesso)
python manage.py migrate

# 4.1 Carregar os dados de exemplo (opcional)
python manage.py loaddata dados_exemplo.json

# 5. Criar um utilizador administrador
python manage.py createsuperuser

# 6. Compilar as traduções
python manage.py compilemessages --ignore=venv

# 7. Arrancar o servidor de desenvolvimento
python manage.py runserver
```

A aplicação fica disponível em **http://127.0.0.1:8000** e a área de administração em **http://127.0.0.1:8000/admin**.

> Em Windows, depois desta configuração inicial, a aplicação pode ser iniciada com um duplo clique no ficheiro `MTR-Gestão.bat`, que ativa o ambiente, arranca o servidor e abre o browser automaticamente.

> **Contas de utilizador:** o superutilizador criado no passo 5 tem acesso completo. Para criar contas de Receção ou Funcionário, usar a página de gestão de utilizadores, atribuindo o grupo correspondente. As contas do perfil Funcionário devem ser associadas ao respetivo registo de funcionário para acederem à área pessoal.

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

---

## Testes

O projeto inclui **44 testes automáticos**, distribuídos por três módulos:

**Marcações (24 testes)**

- *Regras de negócio (7):* aceita marcação válida; recusa sobreposição do mesmo funcionário; recusa mesa já ocupada; aceita marcações seguidas; marcação cancelada liberta o horário; funcionários diferentes em mesas diferentes; edição não colide consigo mesma.
- *Propriedades (5):* `fim` = início + duração do serviço; `em_atraso` quando já passou e continua marcada; `a_decorrer` quando está dentro da duração; marcação futura não está em atraso; marcação realizada nunca está em atraso.
- *Acesso (3):* a agenda e a página de pendentes exigem login e abrem com sessão iniciada.
- *Pendentes antigas (5):* conta as marcações por fechar de dias anteriores; marcações de hoje não contam; marcações antigas já resolvidas não contam; a página lista as pendentes; contas anónimas não recebem contagem.
- *Paginação (4):* primeira e segunda páginas com o número correto de registos; o total reflete todos os registos e não apenas a página; página inválida devolve a última.

**Definições (11 testes)**

- *Modelo (4):* valor por omissão do nome; guardar força sempre o mesmo registo (nunca duplica); não se apaga; idioma e fuso por omissão corretos.
- *Acesso e gravação (4):* exige login; abre com sessão; grava as alterações submetidas; o nome do salão aparece no cabeçalho.
- *Idioma e fuso (3):* mudar o fuso altera a hora apresentada; mudar o idioma altera o nome do mês; a interface fica traduzida.

**Clientes (9 testes)**

- Criação, edição, eliminação e listagem de clientes; validação do formulário; pesquisa por nome; e verificação das rotas.

Para os executar:

```bash
python manage.py test
```

O Django cria uma base de dados temporária, corre os testes e elimina-a no fim. É necessário dar previamente permissão ao utilizador da aplicação sobre essa base:

```sql
GRANT ALL PRIVILEGES ON `test\_salao\_beleza`.* TO 'salao'@'localhost';
FLUSH PRIVILEGES;
```

> **Nota para quem escrever testes novos:** desde a introdução do controlo de acesso por perfis, as contas de teste têm de pertencer a um grupo, caso contrário o middleware bloqueia o acesso e o teste falha. Para as áreas operacionais usa-se `Receção`; para as definições e gestão de utilizadores, `Administrador`.
>
> ```python
> from django.contrib.auth.models import Group, User
>
> utilizador = User.objects.create_user("rececao", password="teste12345")
> utilizador.groups.add(Group.objects.get(name="Receção"))
> self.client.login(username="rececao", password="teste12345")
> ```

---

## Traduções

As traduções ficam em `locale/<idioma>/LC_MESSAGES/django.po`, com os ficheiros compilados (`.mo`) versionados no repositório para que a aplicação funcione sem passos adicionais depois de um `git pull`.

**Para acrescentar textos novos:**

```bash
# 1. Marcar as frases no código
#    Templates: {% load i18n %} e {% trans "Texto" %}
#    Views:     from django.utils.translation import gettext as _
#    Modelos:   from django.utils.translation import gettext_lazy as _

# 2. Recolher as frases para os catálogos
python manage.py makemessages -l pt_PT -l es -l en -l fr --ignore=venv

# 3. Preencher os msgstr vazios nos ficheiros .po

# 4. Compilar
python manage.py compilemessages --ignore=venv
```

> Se uma frase não traduzir depois de compilada, verificar se está marcada como `#, fuzzy` no ficheiro `.po` — o Django ignora traduções aproximadas. Apagar essa linha e recompilar.

---

## Estrutura do projeto

```
Salao-Beleza-MTR/
├── salao/              # Configuração do projeto Django
│   ├── settings.py
│   └── urls.py
├── clientes/           # App: cadastro de clientes
├── funcionarios/       # App: profissionais, horários e ausências
├── utilizadores/       # App: contas, perfis de acesso e área pessoal
├── servicos/           # App: serviços e preçário
├── marcacoes/          # App: marcações e postos (módulo central)
├── mapa/               # App: mapa de ocupação das mesas
├── relatorios/         # App: relatório de serviços por período
├── configuracoes/      # App: definições do salão
├── templates/          # Templates partilhados (base, painel, paginação)
├── locale/             # Catálogos de tradução (pt-pt, es, en, fr)
├── media/              # Ficheiros carregados (fotografias dos funcionários)
├── dados_exemplo.json  # Dados de teste partilhados pela equipa
├── MTR-Gestão.bat      # Atalho de arranque para Windows
├── requirements.txt
└── manage.py
```

> **Convenção de templates:** os templates de cada app ficam em `<app>/templates/<app>/`. A subpasta repetida não é redundante — é o que permite ao Django distinguir ficheiros com o mesmo nome em apps diferentes (por exemplo, `form.html` existe em clientes, serviços e marcações). Sem ela, o Django serve o primeiro que encontrar segundo a ordem de `INSTALLED_APPS`.

---

## Convenções da equipa

**Git e coordenação**

- Cada app tem o seu próprio `app_name` nas rotas.
- `makemigrations` apenas na própria app; quem recebe alterações corre só `migrate`.
- `salao/urls.py`, `salao/settings.py` e `templates/base.html` são partilhados: fazer **Pull antes** de editar e avisar a equipa depois.
- Mensagens de commit em português, sem acentos, verbo no presente ("Adiciona...", "Corrige...", "Atualiza...").
- Nunca fazer *force push*.

**Depois de cada Pull**

```bash
pip install -r requirements.txt
python manage.py migrate
```

**Ao criar uma app nova**

1. Registá-la em `INSTALLED_APPS`.
2. Registá-la em `salao/urls.py`.
3. Colocar os templates em `<app>/templates/<app>/`.
4. Confirmar que os campos indicados no formulário existem no modelo.

**Ao instalar uma biblioteca nova**

Acrescentá-la ao `requirements.txt` no mesmo commit — caso contrário o projeto deixa de arrancar em máquinas onde essa biblioteca não esteja instalada.

---

## Roadmap

**Concluído**

- [x] Configuração do projeto e ligação ao MySQL
- [x] Modelos de dados (Cliente, Serviço, Funcionário, Marcação, Posto, Configuração, Horário de Trabalho, Ausência)
- [x] Área de administração
- [x] Validação de marcações sobrepostas (funcionário e mesa)
- [x] Estrutura base da interface e identidade visual
- [x] Agenda, criação, edição e estados das Marcações
- [x] Navegação por dias e filtro por funcionário na agenda
- [x] Cálculo de horários disponíveis ao marcar
- [x] Marcações em atraso e a decorrer assinaladas no painel
- [x] Aviso e página de marcações por fechar de dias anteriores
- [x] Páginas de Clientes (listar, criar, editar, pesquisar, eliminar)
- [x] Páginas de Serviços e Preçário
- [x] Páginas de Funcionários, com detalhe, filtros, fotografia, horários e ausências
- [x] Autenticação de utilizadores e proteção de todas as páginas
- [x] Perfis de acesso (Administrador, Receção, Funcionário)
- [x] Gestão de contas e alteração da própria palavra-passe
- [x] Área pessoal do funcionário com agenda, horário e resumo do dia
- [x] Relatório de serviços por período
- [x] Mapa de ocupação das mesas
- [x] Painel inicial com indicadores do dia
- [x] Aba de Definições (nome, contactos, horário, idioma, fuso horário)
- [x] Interface traduzida em quatro idiomas (353 frases)
- [x] Paginação da agenda e da lista de pendentes
- [x] Testes automáticos (44)
- [x] Dados de exemplo partilhados
- [x] Atalho de arranque com ícone

**Em curso**

- [ ] Relatórios por perfil: atividade própria no perfil Funcionário; pesquisa por profissional e por cliente no perfil Receção
- [ ] Uniformização da interface (tipografia, ícones, menu lateral, paginação compacta)
- [ ] Reorganização das definições (palavra-passe e gestão de utilizadores)
- [ ] Validação em dispositivos móveis
- [ ] Testes automáticos nos módulos ainda sem cobertura
- [ ] Paginação nas listas de clientes, serviços e funcionários
- [ ] Manual de utilização
- [ ] Preparação da apresentação final

---

## Limitações conhecidas

Esta é uma aplicação de desenvolvimento, com dados fictícios e destinada a ser executada localmente. Para uma colocação em produção seria necessário:

- Mover a chave secreta e as credenciais da base de dados para variáveis de ambiente (`.env`), em vez de as manter no ficheiro de configurações.
- Desativar o modo de depuração (`DEBUG = False`) e definir os domínios autorizados em `ALLOWED_HOSTS`.
- Servir a aplicação através de HTTPS, com cookies seguros e HSTS ativos.
- Substituir o servidor de desenvolvimento por um servidor adequado a produção.
- Alojar localmente os ficheiros do Bootstrap, atualmente carregados de um servidor externo.

O comando `python manage.py check --deploy` lista estes pontos em detalhe.

---

## Equipa

| Nome | Responsabilidades | GitHub |
|---|---|---|
| Rita | Marcações, painel, definições, internacionalização, testes, paginação e gestão do repositório | [@RLair-bit](https://github.com/RLair-bit) |
| Ticiana | Clientes, Serviços e Preçário, relatórios | [@ticianacbd](https://github.com/ticianacbd) |
| Micaele | Funcionários, horários e ausências, autenticação, perfis de acesso, mapa do salão | [@micanatahajlucas-ux](https://github.com/micanatahajlucas-ux) |

---

## Licença

Projeto desenvolvido para fins educativos no âmbito do curso do IEFP Setúbal.
