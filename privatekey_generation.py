from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

# Generate an RSA private key
private_key = rsa.generate_private_key(
    public_exponent=65537,  # Commonly used public exponent value
    key_size=2048,           # Key size (in bits)
    backend=default_backend()
)

# Serialize the private key to PEM format
pem_private_key = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()  # No encryption for private key
)

# Print the private key in PEM format
print(pem_private_key.decode('utf-8'))
