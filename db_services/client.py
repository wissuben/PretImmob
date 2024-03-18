from flask import Response
from db_services.bdd import create_connection, close_connection
import json


def get_clients():
    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM client")
        clients = cursor.fetchall()
        clients_json = json.dumps(clients, default=str)

        # Retourner la réponse en tant que JSON avec le bon en-tête
        return clients_json
    except Exception as e:
        print("Erreur lors de la récupération des clients:", e)
    finally:
        close_connection(connection)


def insert_client(nom_client, password):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        # Exemple de requête d'insertion, ajustez selon vos besoins
        insert_query = """
            INSERT INTO client (nom_client, password)
            VALUES (%s, %s)
        """

        # Exécution de la requête d'insertion avec les valeurs fournies
        cursor.execute(insert_query, (nom_client, password))

        # Valider la transaction
        connection.commit()

    except Exception as e:
        print("Erreur lors de l'insertion du client:", e)
        connection.rollback()


def get_client_by_ID(id_client):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM client WHERE id_client = %s", (id_client,))
        client = cursor.fetchone()
        client_dict = {}
        if client:
            columns = [desc[0] for desc in cursor.description]
            for col, value in zip(columns, client):
                client_dict[col] = value

        return client_dict
    except Exception as e:
        print("Erreur lors de la récupération du client:", e)
    finally:
        close_connection(connection)

