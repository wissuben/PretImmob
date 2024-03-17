from db_services.bdd import create_connection, close_connection
import json


def get_client_history():
    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM client_history")
        client_history = cursor.fetchall()

        client_history_json = json.dumps(client_history, default=str)

        return client_history_json
    except Exception as e:
        print("Erreur lors de la récupération de l'historique client:", e)
    finally:
        close_connection(connection)


def insert_client_history(new_client_history):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        insert_query = """
            INSERT INTO client_history (id_client, debts, late_payments, bankruptcy, loan_amount)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(insert_query, (
            new_client_history['id_client'],
            new_client_history['debts'],
            new_client_history['late_payments'],
            new_client_history['bankruptcy'],
            new_client_history['loan_amount']
        ))

        cursor.execute("SELECT LASTVAL()")
        last_inserted_id = cursor.fetchone()[0]

        connection.commit()

        return last_inserted_id

    except Exception as e:
        print("Erreur lors de l'insertion de l'historique client:", e)
        connection.rollback()
        return -1
    finally:
        close_connection(connection)


def select_client_history_by_id(id_client):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        select_query = """
            SELECT * FROM client_history WHERE id_client = %s
        """

        cursor.execute(select_query, (id_client,))
        client_history = cursor.fetchone()

        client_history_dict = {}
        if client_history:
            columns = [desc[0] for desc in cursor.description]
            for col, value in zip(columns, client_history):
                client_history_dict[col] = value

        return client_history_dict
    except Exception as e:
        print("Erreur lors de la récupération de l'historique client par ID:", e)
        return None

    finally:
        close_connection(connection)


def update_client_history_by_id(id_client, new_client_history):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        update_query = """
            UPDATE client_history
            SET debts = %s,
                late_payments = %s,
                bankruptcy = %s,
                loan_amount = %s
            WHERE id_client = %s
        """

        cursor.execute(update_query, (
            new_client_history['debts'],
            new_client_history['late_payments'],
            new_client_history['bankruptcy'],
            new_client_history['loan_amount'],
            id_client
        ))

        connection.commit()

        return "Mise à jour réussie"
    except Exception as e:
        print("Erreur lors de la mise à jour de l'historique client:", e)
        connection.rollback()
        return "Erreur lors de la mise à jour de l'historique client"
    finally:
        close_connection(connection)
