from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
import base64

def generate_rsa_key_pair():
  private_key = rsa.generate_private_key(
      public_exponent=65537,
      key_size=2048
  )
  public_key = private_key.public_key()
  return private_key, public_key

def export_keys(private_key, public_key):
  private_key_pem = private_key.private_bytes(
      encoding=serialization.Encoding.PEM,
      format=serialization.PrivateFormat.TraditionalOpenSSL,
      encryption_algorithm=serialization.NoEncryption()
  )
  public_key_pem = public_key.public_bytes(
      encoding=serialization.Encoding.PEM,
      format=serialization.PublicFormat.SubjectPublicKeyInfo
  )
  return base64.b64encode(private_key_pem).decode('utf-8'), base64.b64encode(public_key_pem).decode('utf-8')

# Generate and export keys
private_key_pem, public_key_pem = export_keys(*generate_rsa_key_pair())

# Print or send keys securely (e.g., email, secure file transfer)
print(f"Private Key (PEM):\n{private_key_pem}\n")
print(f"Public Key (PEM):\n{public_key_pem}")
