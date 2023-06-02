import json
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

# Generate RSA key pair

private_key = None

if private_key == None:
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096
    )

public_key = private_key.public_key()



def printPublicKey():
    # Serialize and print the public key
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    print("Public Key:")
    print(public_pem.decode('utf-8'))

def printPrivateKey():
    # Serialize and print the private key
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    print("Private Key:")
    print(private_pem.decode('utf-8'))

def savePrivateKey():
    # Serialize and write the private key to pk.txt
    with open("pk.txt", "wb") as file:
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        file.write(private_pem)
        print("Private key saved to file pk.txt")

def returnPrivateKey():
    # Serialize and print the private key
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    return private_pem


def encrypt(data):
    data_json = json.dumps(data)
    # Encrypt the serialized field2
    encrypted = public_key.encrypt(
        data_json.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    encrypted_str = encrypted.hex()
    return encrypted_str

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

def decrypt_as_json(encrypted):
    # Decrypt the encrypted field2
    decrypted_str = decrypt(encrypted)
    decrypted_data = json.loads(decrypted_str)
    return json.dumps(decrypted_data, indent=4)

savePrivateKey()