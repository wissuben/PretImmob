from flask import Response
from bdd import create_connection, close_connection
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


