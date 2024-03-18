from db_services.bdd import create_connection, close_connection
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
            INSERT INTO demande_pret (id_client, nom_client, adresse, email, num_de_tel, montant_pret_demande, 
                                      duree_pret, revenu_mensuel, depenses_mensuelles, statut_demande, description_de_propriete)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Exécution de la requête d'insertion avec les valeurs fournies
        cursor.execute(insert_query, (
            nouvelle_demande['id_client'],
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

        cursor.execute("SELECT LASTVAL()")
        last_inserted_id = cursor.fetchone()[0]

        # Valider la transaction
        connection.commit()

        return last_inserted_id



    except Exception as e:
        print("Erreur lors de l'insertion de la demande de prêt:", e)
        connection.rollback()
        return -1
    finally:
        close_connection(connection)

def select_demande_pret_by_id(id_demande_pret):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        # Requête pour sélectionner une demande de prêt spécifique par son ID
        select_query = """
            SELECT * FROM demande_pret WHERE id_demande_pret = %s
        """

        # Exécution de la requête de sélection avec l'ID fourni
        cursor.execute(select_query, (id_demande_pret,))
        demande_pret = cursor.fetchone()

        demande_pret_dict = {}
        if demande_pret:
            columns = [desc[0] for desc in cursor.description]
            for col, value in zip(columns, demande_pret):
                demande_pret_dict[col] = value

        return demande_pret_dict
    except Exception as e:
        print("Erreur lors de la récupération de la demande de prêt par ID:", e)
        return None
    finally:
        close_connection(connection)

def update_demande_pret_by_id(id_demande_pret, nouvelle_demande):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        # Requête pour mettre à jour une demande de prêt spécifique par son ID
        update_query = """
            UPDATE demande_pret
            SET nom_client = %s,
                adresse = %s,
                email = %s,
                num_de_tel = %s,
                montant_pret_demande = %s,
                duree_pret = %s,
                revenu_mensuel = %s,
                depenses_mensuelles = %s,
                statut_demande = %s,
                description_de_propriete = %s
            WHERE id_demande_pret = %s
        """

        # Exécution de la requête de mise à jour avec les valeurs fournies
        cursor.execute(update_query, (
            nouvelle_demande['nom_client'],
            nouvelle_demande['adresse'],
            nouvelle_demande['email'],
            nouvelle_demande['num_de_tel'],
            nouvelle_demande['montant_pret_demande'],
            nouvelle_demande['duree_pret'],
            nouvelle_demande['revenu_mensuel'],
            nouvelle_demande['depenses_mensuelles'],
            nouvelle_demande['statut_demande'],
            nouvelle_demande['description_de_propriete'],
            id_demande_pret
        ))

        # Valider la transaction
        connection.commit()

        return "Mise à jour réussie"
    except Exception as e:
        print("Erreur lors de la mise à jour de la demande de prêt:", e)
        connection.rollback()
        return "Erreur lors de la mise à jour de la demande de prêt"
    finally:
        close_connection(connection)

def update_scoring_by_id(id_demande_pret, scoring):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        # Requête pour mettre à jour le score d'une demande de prêt spécifique par son ID
        update_query = """
            UPDATE demande_pret
            SET scoring = %s
            WHERE id_demande_pret = %s
        """

        # Exécution de la requête de mise à jour avec le score fourni
        cursor.execute(update_query, (scoring, id_demande_pret))

        # Valider la transaction
        connection.commit()

        return "Mise à jour du score réussie"
    except Exception as e:
        print("Erreur lors de la mise à jour du score de la demande de prêt:", e)
        connection.rollback()
        return "Erreur lors de la mise à jour du score de la demande de prêt"
    finally:
        close_connection(connection)

def update_solvency_by_id(id_demande_pret, solvency):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        # Requête pour mettre à jour la solvabilité d'une demande de prêt spécifique par son ID
        update_query = """
            UPDATE demande_pret
            SET solvency = %s
            WHERE id_demande_pret = %s
        """

        # Exécution de la requête de mise à jour avec la solvabilité fournie
        cursor.execute(update_query, (solvency, id_demande_pret))

        # Valider la transaction
        connection.commit()

        return "Mise à jour de la solvabilité réussie"
    except Exception as e:
        print("Erreur lors de la mise à jour de la solvabilité de la demande de prêt:", e)
        connection.rollback()
        return "Erreur lors de la mise à jour de la solvabilité de la demande de prêt"
    finally:
        close_connection(connection)

def update_property_valuation_by_id(id_demande_pret, property_valuation):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        # Requête pour mettre à jour l'évaluation de propriété d'une demande de prêt spécifique par son ID
        update_query = """
            UPDATE demande_pret
            SET property_valuation = %s
            WHERE id_demande_pret = %s
        """

        # Exécution de la requête de mise à jour avec l'évaluation de propriété fournie
        cursor.execute(update_query, (property_valuation, id_demande_pret))

        # Valider la transaction
        connection.commit()

        return "Mise à jour de l'évaluation de propriété réussie"
    except Exception as e:
        print("Erreur lors de la mise à jour de l'évaluation de propriété de la demande de prêt:", e)
        connection.rollback()
        return "Erreur lors de la mise à jour de l'évaluation de propriété de la demande de prêt"
    finally:
        close_connection(connection)

def update_decision_by_id(id_demande_pret, decision):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        # Requête pour mettre à jour la décision d'une demande de prêt spécifique par son ID
        update_query = """
            UPDATE demande_pret
            SET decision = %s
            WHERE id_demande_pret = %s
        """

        # Exécution de la requête de mise à jour avec la décision fournie
        cursor.execute(update_query, (decision, id_demande_pret))

        # Valider la transaction
        connection.commit()

        return "Mise à jour de la décision réussie"
    except Exception as e:
        print("Erreur lors de la mise à jour de la décision de la demande de prêt:", e)
        connection.rollback()
        return "Erreur lors de la mise à jour de la décision de la demande de prêt"
    finally:
        close_connection(connection)

