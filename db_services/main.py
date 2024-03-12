from client import *
from client_history import get_client_history
from demande_pret import get_demandes_pret, insert_demande_pret

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
print(insert_demande_pret(patterns))
print(get_demandes_pret())