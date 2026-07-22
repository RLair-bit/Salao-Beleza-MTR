from pathlib import Path

import polib


BASE_DIR = Path(__file__).resolve().parent


TRADUCOES = {
    "en": {
        "Funcionários": "Staff",
        "Novo funcionário": "New staff member",
        "Procurar por nome...": "Search by name...",
        "Todos os estados": "All statuses",
        "Apenas ativos": "Active only",
        "Apenas inativos": "Inactive only",
        "Filtrar": "Filter",
        "Nome": "Name",
        "Função": "Role",
        "Serviços": "Services",
        "Estado": "Status",
        "Ações": "Actions",
        "Ativo": "Active",
        "Inativo": "Inactive",
        "Ver": "View",
        "Editar": "Edit",
        "Eliminar": "Delete",
        "Ainda não há funcionários registados.": (
            "No staff members have been registered yet."
        ),
        "Detalhes do funcionário": "Staff details",
        "Não indicado": "Not provided",
        "Não indicada": "Not provided",
        "Não definido": "Not defined",
        "Voltar": "Back",
        "Informações profissionais": "Professional information",
        "Telefone": "Phone",
        "Serviços que presta": "Services provided",
        "Nenhum serviço associado.": "No services assigned.",
        "Marcações": "Appointments",
        "Próximas marcações": "Upcoming appointments",
        "Data": "Date",
        "Horário": "Time",
        "Cliente": "Client",
        "Serviço": "Service",
        "Mesa/Posto": "Table/Station",
        "Não existem marcações futuras para esta funcionária.": (
            "There are no upcoming appointments for this staff member."
        ),
        "Editar funcionário": "Edit staff member",
        "Guardar": "Save",
        "Cancelar": "Cancel",
        "Eliminar funcionário": "Delete staff member",
        "Tens a certeza de que queres eliminar <b>%(nome)s</b>?": (
            "Are you sure you want to delete <b>%(nome)s</b>?"
        ),
        "Sim, eliminar": "Yes, delete",
        "Entrar": "Log in",
        "Utilizador ou password incorretos.": (
            "Incorrect username or password."
        ),
        "Utilizador": "Username",
        "Password": "Password",
        "Mapa do Salão": "Salon Map",
        "Mapa do Salão — %(data)s": "Salon Map — %(data)s",
        "Total de mesas": "Total tables",
        "Mesas ocupadas": "Occupied tables",
        "Mesas livres": "Available tables",
        "Marcações do dia": "Appointments today",
        "Dia": "Day",
        "Livre": "Available",
        "Sem marcações neste dia.": "No appointments on this day.",
        "Funcionário criado com sucesso.": (
            "Staff member created successfully."
        ),
        "Funcionário atualizado.": "Staff member updated.",
        "Funcionário eliminado.": "Staff member deleted.",
        (
            "Não é possível eliminar: este funcionário tem "
            "marcações associadas. Em alternativa, desativa-o."
        ): (
            "This staff member cannot be deleted because they have "
            "associated appointments. Deactivate them instead."
        ),
    },

    "es": {
        "Funcionários": "Personal",
        "Novo funcionário": "Nuevo empleado",
        "Procurar por nome...": "Buscar por nombre...",
        "Todos os estados": "Todos los estados",
        "Apenas ativos": "Solo activos",
        "Apenas inativos": "Solo inactivos",
        "Filtrar": "Filtrar",
        "Nome": "Nombre",
        "Função": "Función",
        "Serviços": "Servicios",
        "Estado": "Estado",
        "Ações": "Acciones",
        "Ativo": "Activo",
        "Inativo": "Inactivo",
        "Ver": "Ver",
        "Editar": "Editar",
        "Eliminar": "Eliminar",
        "Ainda não há funcionários registados.": (
            "Todavía no hay empleados registrados."
        ),
        "Detalhes do funcionário": "Detalles del empleado",
        "Não indicado": "No indicado",
        "Não indicada": "No indicada",
        "Não definido": "No definido",
        "Voltar": "Volver",
        "Informações profissionais": "Información profesional",
        "Telefone": "Teléfono",
        "Serviços que presta": "Servicios que presta",
        "Nenhum serviço associado.": "Ningún servicio asociado.",
        "Marcações": "Citas",
        "Próximas marcações": "Próximas citas",
        "Data": "Fecha",
        "Horário": "Horario",
        "Cliente": "Cliente",
        "Serviço": "Servicio",
        "Mesa/Posto": "Mesa/Puesto",
        "Não existem marcações futuras para esta funcionária.": (
            "No existen próximas citas para esta empleada."
        ),
        "Editar funcionário": "Editar empleado",
        "Guardar": "Guardar",
        "Cancelar": "Cancelar",
        "Eliminar funcionário": "Eliminar empleado",
        "Tens a certeza de que queres eliminar <b>%(nome)s</b>?": (
            "¿Estás seguro de que quieres eliminar "
            "<b>%(nome)s</b>?"
        ),
        "Sim, eliminar": "Sí, eliminar",
        "Entrar": "Iniciar sesión",
        "Utilizador ou password incorretos.": (
            "Usuario o contraseña incorrectos."
        ),
        "Utilizador": "Usuario",
        "Password": "Contraseña",
        "Mapa do Salão": "Mapa del salón",
        "Mapa do Salão — %(data)s": "Mapa del salón — %(data)s",
        "Total de mesas": "Total de mesas",
        "Mesas ocupadas": "Mesas ocupadas",
        "Mesas livres": "Mesas libres",
        "Marcações do dia": "Citas del día",
        "Dia": "Día",
        "Livre": "Libre",
        "Sem marcações neste dia.": "No hay citas este día.",
        "Funcionário criado com sucesso.": (
            "Empleado creado correctamente."
        ),
        "Funcionário atualizado.": "Empleado actualizado.",
        "Funcionário eliminado.": "Empleado eliminado.",
        (
            "Não é possível eliminar: este funcionário tem "
            "marcações associadas. Em alternativa, desativa-o."
        ): (
            "No se puede eliminar: este empleado tiene citas "
            "asociadas. Como alternativa, desactívalo."
        ),
    },

    "fr": {
        "Funcionários": "Personnel",
        "Novo funcionário": "Nouveau membre du personnel",
        "Procurar por nome...": "Rechercher par nom...",
        "Todos os estados": "Tous les statuts",
        "Apenas ativos": "Actifs uniquement",
        "Apenas inativos": "Inactifs uniquement",
        "Filtrar": "Filtrer",
        "Nome": "Nom",
        "Função": "Fonction",
        "Serviços": "Services",
        "Estado": "Statut",
        "Ações": "Actions",
        "Ativo": "Actif",
        "Inativo": "Inactif",
        "Ver": "Voir",
        "Editar": "Modifier",
        "Eliminar": "Supprimer",
        "Ainda não há funcionários registados.": (
            "Aucun membre du personnel n'est encore enregistré."
        ),
        "Detalhes do funcionário": (
            "Détails du membre du personnel"
        ),
        "Não indicado": "Non indiqué",
        "Não indicada": "Non indiquée",
        "Não definido": "Non défini",
        "Voltar": "Retour",
        "Informações profissionais": (
            "Informations professionnelles"
        ),
        "Telefone": "Téléphone",
        "Serviços que presta": "Services proposés",
        "Nenhum serviço associado.": "Aucun service associé.",
        "Marcações": "Rendez-vous",
        "Próximas marcações": "Prochains rendez-vous",
        "Data": "Date",
        "Horário": "Horaire",
        "Cliente": "Client",
        "Serviço": "Service",
        "Mesa/Posto": "Table/Poste",
        "Não existem marcações futuras para esta funcionária.": (
            "Il n'y a aucun rendez-vous à venir pour cette employée."
        ),
        "Editar funcionário": (
            "Modifier le membre du personnel"
        ),
        "Guardar": "Enregistrer",
        "Cancelar": "Annuler",
        "Eliminar funcionário": (
            "Supprimer le membre du personnel"
        ),
        "Tens a certeza de que queres eliminar <b>%(nome)s</b>?": (
            "Êtes-vous sûr de vouloir supprimer "
            "<b>%(nome)s</b> ?"
        ),
        "Sim, eliminar": "Oui, supprimer",
        "Entrar": "Se connecter",
        "Utilizador ou password incorretos.": (
            "Nom d'utilisateur ou mot de passe incorrect."
        ),
        "Utilizador": "Utilisateur",
        "Password": "Mot de passe",
        "Mapa do Salão": "Plan du salon",
        "Mapa do Salão — %(data)s": "Plan du salon — %(data)s",
        "Total de mesas": "Nombre total de tables",
        "Mesas ocupadas": "Tables occupées",
        "Mesas livres": "Tables libres",
        "Marcações do dia": "Rendez-vous du jour",
        "Dia": "Jour",
        "Livre": "Libre",
        "Sem marcações neste dia.": (
            "Aucun rendez-vous ce jour-là."
        ),
        "Funcionário criado com sucesso.": (
            "Membre du personnel créé avec succès."
        ),
        "Funcionário atualizado.": (
            "Membre du personnel mis à jour."
        ),
        "Funcionário eliminado.": (
            "Membre du personnel supprimé."
        ),
        (
            "Não é possível eliminar: este funcionário tem "
            "marcações associadas. Em alternativa, desativa-o."
        ): (
            "Impossible de supprimer : ce membre du personnel a "
            "des rendez-vous associés. Vous pouvez le désactiver "
            "à la place."
        ),
    },

    "pt_PT": {
        "Funcionários": "Funcionários",
        "Novo funcionário": "Novo funcionário",
        "Procurar por nome...": "Procurar por nome...",
        "Todos os estados": "Todos os estados",
        "Apenas ativos": "Apenas ativos",
        "Apenas inativos": "Apenas inativos",
        "Filtrar": "Filtrar",
        "Nome": "Nome",
        "Função": "Função",
        "Serviços": "Serviços",
        "Estado": "Estado",
        "Ações": "Ações",
        "Ativo": "Ativo",
        "Inativo": "Inativo",
        "Ver": "Ver",
        "Editar": "Editar",
        "Eliminar": "Eliminar",
        "Ainda não há funcionários registados.": (
            "Ainda não há funcionários registados."
        ),
        "Detalhes do funcionário": "Detalhes do funcionário",
        "Não indicado": "Não indicado",
        "Não indicada": "Não indicada",
        "Não definido": "Não definido",
        "Voltar": "Voltar",
        "Informações profissionais": (
            "Informações profissionais"
        ),
        "Telefone": "Telefone",
        "Serviços que presta": "Serviços que presta",
        "Nenhum serviço associado.": (
            "Nenhum serviço associado."
        ),
        "Marcações": "Marcações",
        "Próximas marcações": "Próximas marcações",
        "Data": "Data",
        "Horário": "Horário",
        "Cliente": "Cliente",
        "Serviço": "Serviço",
        "Mesa/Posto": "Mesa/Posto",
        "Não existem marcações futuras para esta funcionária.": (
            "Não existem marcações futuras para esta funcionária."
        ),
        "Editar funcionário": "Editar funcionário",
        "Guardar": "Guardar",
        "Cancelar": "Cancelar",
        "Eliminar funcionário": "Eliminar funcionário",
        "Tens a certeza de que queres eliminar <b>%(nome)s</b>?": (
            "Tens a certeza de que queres eliminar "
            "<b>%(nome)s</b>?"
        ),
        "Sim, eliminar": "Sim, eliminar",
        "Entrar": "Entrar",
        "Utilizador ou password incorretos.": (
            "Utilizador ou password incorretos."
        ),
        "Utilizador": "Utilizador",
        "Password": "Password",
        "Mapa do Salão": "Mapa do Salão",
        "Mapa do Salão — %(data)s": "Mapa do Salão — %(data)s",
        "Total de mesas": "Total de mesas",
        "Mesas ocupadas": "Mesas ocupadas",
        "Mesas livres": "Mesas livres",
        "Marcações do dia": "Marcações do dia",
        "Dia": "Dia",
        "Livre": "Livre",
        "Sem marcações neste dia.": "Sem marcações neste dia.",
        "Funcionário criado com sucesso.": (
            "Funcionário criado com sucesso."
        ),
        "Funcionário atualizado.": "Funcionário atualizado.",
        "Funcionário eliminado.": "Funcionário eliminado.",
        (
            "Não é possível eliminar: este funcionário tem "
            "marcações associadas. Em alternativa, desativa-o."
        ): (
            "Não é possível eliminar: este funcionário tem "
            "marcações associadas. Em alternativa, desativa-o."
        ),
    },
}


PLURAIS = {
    "en": {
        0: "appointment associated",
        1: "appointments associated",
    },
    "es": {
        0: "cita asociada",
        1: "citas asociadas",
    },
    "fr": {
        0: "rendez-vous associé",
        1: "rendez-vous associés",
    },
    "pt_PT": {
        0: "marcação associada",
        1: "marcações associadas",
    },
}


def atualizar_entrada(po, msgid, msgstr):
    entrada = po.find(msgid)

    if entrada is None:
        entrada = polib.POEntry(
            msgid=msgid,
            msgstr=msgstr,
        )
        po.append(entrada)
    else:
        entrada.msgstr = msgstr

    if "fuzzy" in entrada.flags:
        entrada.flags.remove("fuzzy")


def atualizar_plural(po, traducoes):
    msgid = "marcação associada"
    msgid_plural = "marcações associadas"

    entrada = po.find(msgid)

    if entrada is None:
        entrada = polib.POEntry(
            msgid=msgid,
            msgid_plural=msgid_plural,
            msgstr_plural=traducoes,
        )
        po.append(entrada)
    else:
        entrada.msgid_plural = msgid_plural
        entrada.msgstr_plural = traducoes

    if "fuzzy" in entrada.flags:
        entrada.flags.remove("fuzzy")


def main():
    for idioma, traducoes in TRADUCOES.items():
        pasta = BASE_DIR / "locale" / idioma / "LC_MESSAGES"
        ficheiro_po = pasta / "django.po"
        ficheiro_mo = pasta / "django.mo"

        if not ficheiro_po.exists():
            print(f"Ficheiro não encontrado: {ficheiro_po}")
            continue

        po = polib.pofile(str(ficheiro_po))

        for msgid, msgstr in traducoes.items():
            atualizar_entrada(po, msgid, msgstr)

        atualizar_plural(po, PLURAIS[idioma])

        po.save(str(ficheiro_po))
        po.save_as_mofile(str(ficheiro_mo))

        print(f"Traduções atualizadas: {idioma}")

    print("Processo concluído com sucesso.")


if __name__ == "__main__":
    main()