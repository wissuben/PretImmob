from flask import Response
from bdd import create_connection, close_connection
import json



def get_client_history():
    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM client_history")
        client_history = cursor.fetchall()

        clients_history_json = json.dumps(client_history, default=str)

        # Retourner la réponse en tant que JSON avec le bon en-tête
        return clients_history_json


    except Exception as e:
        print("Erreur lors de la récupération de l'historique des clients:", e)
    finally:
        close_connection(connection)


