import hashlib

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

def verify_password(password, key, hashed_password):
    """Verifies if the provided password corresponds to the given hashed password and key."""
    # Hash the provided password using the same key
    hashed_input = hash_password(password, key)
    # Compare the hashed input with the provided hashed password
    return hashed_input == hashed_password

# Example usage:
password = "wissuwissu"
key = "somesecretkey"

# Hash the password using the key
hashed_password = hash_password(password, key)
print("Hashed password:", hashed_password)

hashed_password = hash_password(password, key)
print("Hashed password:", hashed_password)

# Verify if a provided password matches the hashed password
input_password = "mysecretpassword"
if verify_password(input_password, key, hashed_password):
    print("Password is correct!")
else:
    print("Incorrect password!")
