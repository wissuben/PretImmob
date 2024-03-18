import hashlib

from passlib.context import CryptContext
from db_services.client import insert_client, get_client_by_ID

# Initialisation du contexte de hachage avec l'algorithme bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
key = "somesecretkey"


def hash_password(password, key):
    """Hashes the password using a key."""
    # Concatenate the password and the key
    combined_str = password + key
    # Encode the string to bytes
    combined_bytes = combined_str.encode('utf-8')
    # Hash the bytes using SHA-256
    hashed_bytes = hashlib.sha256(combined_bytes)
    # Return the hexadecimal representation of the hash
    return hashed_bytes.hexdigest()


def populate_client_table_with_hashed_passwords():
    # Données des clients avec des mots de passe en clair
    clients_data = [
        {"nom_client": "Doe", "password": "motdepasse123"},
        {"nom_client": "wissal benharouga", "password": "wissuwissu"},
        {"nom_client": "John", "password": "test"},
        # Ajoutez d'autres utilisateurs ici...
    ]

    # Insérer chaque client dans la base de données avec le mot de passe haché
    for client_data in clients_data:
        hashed_password = hash_password(client_data["password"], key)
        insert_client(client_data["nom_client"], hashed_password)


def verify_password(password, key, hashed_password):
    """Verifies if the provided password corresponds to the given hashed password and key."""
    # Hash the provided password using the same key
    hashed_input = hash_password(password, key)
    # Compare the hashed input with the provided hashed password
    return hashed_input == hashed_password


def authenticate_user(id_client, password):
    # Récupérer le client par son nom
    client = get_client_by_ID(id_client)
    print(client)
    if client is not None and isinstance(client, dict):
        # Si le client existe et est un dictionnaire
        hashed_password = client.get("password")  # Utilisez .get() pour obtenir la valeur sans provoquer d'erreur
        if hashed_password:
            return verify_password(password, key, hashed_password)
    return False


if __name__ == "__main__":
    populate_client_table_with_hashed_passwords()
