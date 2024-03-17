from client import *
from client_history import get_client_history
from demande_pret import get_demandes_pret, insert_demande_pret, select_demande_pret_by_id, update_demande_pret_by_id, update_scoring_by_id, update_solvency_by_id


print(get_clients())

patterns = {
                'nom_client': "1",
                'adresse': "velizy",
                'email': "lolo@gmail.com",
                'num_de_tel': "0677777777",
                'montant_pret_demande': "10000",
                'duree_pret': "5",
                'revenu_mensuel': "1234",
                'depenses_mensuelles': "123",
                'statut_demande': "pending",
                'description_de_propriete': "jardin"
            }
#print(insert_demande_pret(patterns))
print(get_demandes_pret())
print(select_demande_pret_by_id(10))

patterns = {
                'nom_client': "1",
                'adresse': "eljadida",
                'email': "lolo@gmail.com",
                'num_de_tel': "0677777777",
                'montant_pret_demande': "10000",
                'duree_pret': "5",
                'revenu_mensuel': "1234",
                'depenses_mensuelles': "123",
                'statut_demande': "pending",
                'description_de_propriete': "jardin"
            }

print(update_demande_pret_by_id(10, patterns))
print(select_demande_pret_by_id(10))
update_solvency_by_id(10, True)
update_scoring_by_id(10, 50)
print(select_demande_pret_by_id(10))

