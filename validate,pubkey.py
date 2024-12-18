import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

# Sample public key (replace this with the actual RSA public key data in PEM format)
SAMPLE_PUBLIC_KEY_DATA = b"""
-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEA29KSK0pGzZB94ffnLASN07XbqY/lyWDWS3MZYDeMQcseRcH3y2/F
oDdwGNvxIpnQnaJNCXMBtDp1x9B3JFCmG/K9E6L84nKgq9gD/xVjKgPL11hduwD0
Jxj+/DqUz+PhlI7LtkuGTSn0mTLiJZL433okMgG2fza7v+/dXrrBu7GX1U/eShXT
IJRGE9ttCY340BqiIVctiw/VedZMMcRAiuELwW7ubTFWmHd+nel8Kn3JFHMefDnFo
F05pj4qmkHzy4cM34w5EOQggK+GflH6L9vsSINuG0Swdy2iGaJB2Mk6kALZbDEbAh
edlceA/khMUOK4IVKRCEkke7jPgdIKiQIDAQAB
-----END RSA PUBLIC KEY-----
"""

def validate_signed_document(file_path, public_key_data):
    try:
        # Load the RSA public key from PEM format
        public_key = serialization.load_pem_public_key(
            public_key_data
        )

        # Read the signed document
        with open(file_path, "rb") as file:
            document_data = file.read()

        # Extract the original document data and signature
        original_document = document_data[:-public_key.key_size // 8]
        signature = document_data[-public_key.key_size // 8:]

        # Compute SHA-256 hash of the original document
        hash_algorithm = hashes.SHA256()
        hash_value = hashes.Hash(hash_algorithm)
        hash_value.update(original_document)
        digest = hash_value.finalize()

        # Verify the signature using the public key
        public_key.verify(
            signature,
            digest,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            algorithm=hash_algorithm
        )

        messagebox.showinfo("Validation Result", "Document signature is VALID")

    except Exception as e:
        messagebox.showerror("Validation Result", "Document signature is INVALID")

def browse_file_and_validate():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
    if file_path:
        validate_signed_document(file_path, SAMPLE_PUBLIC_KEY_DATA)

# Create the main window
root = tk.Tk()
root.title("Digital Document Validator")

# Create a button to browse, select, and validate a signed document
validate_button = tk.Button(root, text="Browse Signed Document and Validate", command=browse_file_and_validate)
validate_button.pack(pady=20)

# Run the main event loop
root.mainloop()
