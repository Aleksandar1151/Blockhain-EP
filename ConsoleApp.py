import json

import pem
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

# RSA_Class.savePrivateKey()
# privateKey = RSA_Class.returnPrivateKey()

# Prompt the user to enter the JSON file name
file_name = input("Naziv JSON fajla: ")

# print(privateKey.decode('utf-8'))
# Load JSON file
with open(file_name, "r") as file:
    json_data = json.load(file)

# Load private key from file
with open('pk.txt', 'rb') as f:
    key_data = f.read()
private_key_from_file = pem.parse(key_data)[0].as_text()
private_key = serialization.load_pem_private_key(key_data, password=None)
def decrypt_as_json(encrypted):
    # Decrypt the encrypted field2
    decrypted_str = decrypt(encrypted)
    decrypted_data = json.loads(decrypted_str)
    return json.dumps(decrypted_data, indent=4)

def decrypt(encrypted):
    # Convert the hex-encoded string back to bytes
    encrypted_bytes = bytes.fromhex(encrypted)
    # Decrypt the encrypted field2
    decrypted = private_key.decrypt(
        encrypted_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    decrypted_str = decrypted.decode('utf-8')
    return decrypted_str

# Extract "data" field
data_value = json_data["data"]
decrypted_data_json = decrypt_as_json(json_data["data"])

print(decrypted_data_json)




