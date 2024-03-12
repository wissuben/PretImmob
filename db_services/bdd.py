import psycopg2

def create_connection():
    try:
        connection = psycopg2.connect(
            user="soadb_user",
            password="NpMMkmYzumW1ZyhPkExYYdDjz0FzXV6B",
            host="dpg-cnlqbb6v3ddc73fj2no0-a.oregon-postgres.render.com",
            port="5432",
            database="soadb"
        )
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Erreur lors de la connexion à la base de données:", error)

def close_connection(connection):
    if connection:
        connection.close()
        print("Connexion à la base de données fermée.")
