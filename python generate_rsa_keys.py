from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

def generate_rsa_key_pair(key_size=2048):
    # Generate RSA private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,  # Recommended value for RSA
        key_size=key_size,      # Key size (bits)
    )

    # Get the corresponding public key
    public_key = private_key.public_key()

    # Serialize private key to PEM format
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Serialize public key to PEM format
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_key_pem, public_key_pem

def save_keys_to_files(private_key_pem, public_key_pem):
    # Write private key to a file
    with open("private_key.pem", "wb") as private_key_file:
        private_key_file.write(private_key_pem)
    print("Private key saved to private_key.pem")

    # Write public key to a file
    with open("public_key.pem", "wb") as public_key_file:
        public_key_file.write(public_key_pem)
    print("Public key saved to public_key.pem")

if __name__ == "__main__":
    # Generate RSA key pair
    private_key_pem, public_key_pem = generate_rsa_key_pair()

    # Save keys to files
    save_keys_to_files(private_key_pem, public_key_pem)
