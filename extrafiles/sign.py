import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
import sys

# Sample private key (replace this with your actual RSA private key data in PEM format)
SAMPLE_PRIVATE_KEY_DATA = b"""
-----BEGIN RSA PRIVATE KEY-----
MIIEoAIBAAKCAQEA29KSK0pGzZB94ffnLASN07XbqY/lyWDWS3MZYDeMQcseRcH3
y2/FoDdwGNvxIpnQnaJNCXMBtDp1x9B3JFCmG/K9E6L84nKgq9gD/xVjKgPL11hd
uwD0Jxj+/DqUz+PhlI7LtkuGTSn0mTLiJZL433okMgG2fza7v+/dXrrBu7GX1U/e
ShXTIJRGE9ttCY340BqiIVctiw/VedZMMcRAiuELwW7ubTFWmHd+nel8Kn3JFHMe
fDnFoF05pj4qmkHzy4cM34w5EOQggK+GflH6L9vsSINuG0Swdy2iGaJB2Mk6kALZ
bDEbAhedlceA/khMUOK4IVKRCEkke7jPgdIKiQIDAQABAoH/S/gUejoma0zd7Xg4
YXE1Z1a+BLFS7MqNo0iTJtfMoidzyezPwS0vY1Hs0wkQZYVWpj9IpVT1OujN6SO5
FPBf+civ8/D+ndWjEe+9/542T4MOI5Y8GThjhxO+3FMAFPQraP+lwADZ5EkocW7w
MRXzl+2HpoGUe87SEgIzEcvpZU1nZlCk9u4eymfjUJM4LBIji2NNniifzgm+W47b
bY2rAPkbArPsy1eN1tYCUGlowZMGVGA0cBPa2saZH1kPFoKiG+1MMbosB0IQ3Ej3
p94ie8BkmxYHTUsK1dNSVwPonfk/6nd+c2wdD+nK1i0a5X5qzow+La8Ds7wAD8Ew
LanhAoGBAPtrGFyb//niGI/fbR3PpHqxizAOgC5Q2Sm0fwu+usZMbGAjdUAgSrdZ
q7T/Hw8zbqtko87cYkFs4A7otBuq0zrhHNtDb18HwI64nlIyGDnkb4iLZM59mdNo
RE783KxpNoLJmiVTsItY3KMNpd/T4s6+Z1ddpv4148YBASt7Fn4ZAoGBAN/UE5xK
92NOQWQaOp3cSjGm+tuup93S1ZBlFOFWTg4SWu98B7CI02gzN6TFoFilu0rK1zDe
eJieap5A1ArCKOptmJfkADEuhfSNnX5SM01AR1ILcHSrqSIFMzClXMC775AhazOJ
zcblBAWYJeTMNDdhPLj/LZHFwb53r/Cy0J3xAoGAKDVDayQjtuHazb+MotTfWCPm
v6PCCiYx5MKSAt3Y3ve/6UwiZ0QCzvnPRR376KFwFIb+z4ldSVtRJfE/RKF4MJVp
2QMa35bMy8Zow3pxd2i6EZtBXuilXjLxobQ80nHtHtOBDHEq7c4jUwxOt9IaFrhK
rKU0nLkfmT314u9HdJkCgYAWxfEo2cfJ5tBoavLD1QIHg0HK0D5sJ2NrSZ2SP8G5
VMzDyQ7PO1ynIW7r6N+jpVklBvZWFoyWmqemaloorhCTqYr5CU2rs1wVwcLgc2Sc
24lmI5vRgxW2TGkk7e49/eEl/QB3QfIZ5ns+Rni0isJVUCNpfy0Xw9MumebgypDH
QQKBgF+GGQATWd9ay0AImDmfXREQSuLwd1r7kNdN6M1CzCOHUHi+1Wp7XPbKafPD
+6VWSZdXae61WhWGlAjqbuH+cPHgxn17JteHEltGwwuzExUSKeNQCmKHQ6oDIQzi
YGzs8uTqGweB2bBkiYyZ4UBk2sT8V8dG/CoMef5zGf92QFAC
-----END RSA PRIVATE KEY-----
"""

def sign_document(file_path):
    try:
        # Load the RSA private key from PEM format
        private_key = serialization.load_pem_private_key(
            SAMPLE_PRIVATE_KEY_DATA,
            password=None  # Assuming no password protection
        )

        # Read the document data in binary mode
        with open(file_path, "rb") as file:
            document_data = file.read()

        # Compute SHA-256 hash of the document
        hash_algorithm = hashes.SHA256()
        hash_value = hashes.Hash(hash_algorithm)
        hash_value.update(document_data)
        digest = hash_value.finalize()

        # Sign the hash digest
        signature = private_key.sign(
            digest,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            algorithm=hash_algorithm
        )
        

        # Determine the output file path for the signed document
        signed_file_path = file_path[:-4] + "_signed.pdf"  # Assuming the input file is a PDF

        # Write the signed document to the output file
        with open(signed_file_path, "wb") as signed_file:
            signed_file.write(document_data)
            signed_file.write(signature)

        messagebox.showinfo("Success", f"Document signed and saved as {signed_file_path}")
        

    except Exception as e:
        messagebox.showerror("Error", f"Failed to sign document: {e}")

if __name__ == "__main__":
    # Call sign_document function with the provided file path
    file_path = sys.argv[1]
    sign_document(file_path)