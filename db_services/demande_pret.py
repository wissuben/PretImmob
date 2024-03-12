from bdd import create_connection, close_connection
import json


def get_demandes_pret():
    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM demande_pret")
        demandes_pret = cursor.fetchall()

        demandes_pret_json = json.dumps(demandes_pret, default=str)

        # Retourner la réponse en tant que JSON avec le bon en-tête
        return demandes_pret_json
    except Exception as e:
        print("Erreur lors de la récupération des demandes de prêt:", e)
    finally:
        close_connection(connection)

def insert_demande_pret(nouvelle_demande):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        # Exemple de requête d'insertion, ajustez selon vos besoins
        insert_query = """
            INSERT INTO demande_pret (nom_client, adresse, email, num_de_tel, montant_pret_demande, 
                                      duree_pret, revenu_mensuel, depenses_mensuelles, statut_demande, description_de_propriete)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Exécution de la requête d'insertion avec les valeurs fournies
        cursor.execute(insert_query, (
            nouvelle_demande['nom_client'],
            nouvelle_demande['adresse'],
            nouvelle_demande['email'],
            nouvelle_demande['num_de_tel'],
            nouvelle_demande['montant_pret_demande'],
            nouvelle_demande['duree_pret'],
            nouvelle_demande['revenu_mensuel'],
            nouvelle_demande['depenses_mensuelles'],
            nouvelle_demande['statut_demande'],
            nouvelle_demande['description_de_propriete']
        ))

        last_inserted_id = cursor.lastrowid


        # Valider la transaction
        connection.commit()

        return last_inserted_id
    except Exception as e:
        print("Erreur lors de l'insertion de la demande de prêt:", e)
        connection.rollback()
        return -1
    finally:
        close_connection(connection)