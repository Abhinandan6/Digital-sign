import os
import json
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

PHP_SCRIPT_PATH = 'new,fetchkeys.php'  # Path to your PHP script

def fetch_keys():
    result = subprocess.run(['php', PHP_SCRIPT_PATH], capture_output=True, text=True)
    if result.returncode == 0:
        keys = json.loads(result.stdout)
        if 'error' in keys:
            raise Exception(keys['error'])
        return keys['private_key'], keys['public_key']
    else:
        raise Exception("Failed to fetch keys from PHP script.")

def sign_document(file_path):
    try:
        private_key_pem, _ = fetch_keys()

        # Load the RSA private key from PEM format
        private_key = serialization.load_pem_private_key(
            private_key_pem.encode(),
            password=None
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
        signed_file_path = file_path[:-4] + "_signed" + file_path[-4:]  # Maintain the file extension

        # Write the signed document to the output file
        with open(signed_file_path, "wb") as signed_file:
            signed_file.write(document_data)
            signed_file.write(signature)

        messagebox.showinfo("Success", f"Document signed and saved as {signed_file_path}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to sign document: {e}")

def validate_signed_document(file_path):
    try:
        _, public_key_pem = fetch_keys()

        # Load the RSA public key from PEM format
        public_key = serialization.load_pem_public_key(
            public_key_pem.encode()
        )

        # Read the signed document
        with open(file_path, "rb") as file:
            document_data = file.read()

        # Extract the original document data and signature
        signature = document_data[-public_key.key_size // 8:]
        original_document = document_data[:-public_key.key_size // 8]

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
        messagebox.showerror("Validation Result", f"Document signature is INVALID: {e}")

def browse_file_and_sign():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", ".pdf"), ("All files", ".*")])
    if file_path:
        sign_document(file_path)

def browse_file_and_validate():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", ".pdf"), ("All files", ".*")])
    if file_path:
        validate_signed_document(file_path)

# Create the main window
root = tk.Tk()
root.title("Digital Document Signer and Validator")

# Create a button to browse, select, and sign a document
sign_button = tk.Button(root, text="Browse Document and Sign", command=browse_file_and_sign)
sign_button.pack(pady=10)

# Create a button to browse, select, and validate a signed document
validate_button = tk.Button(root, text="Browse Signed Document and Validate", command=browse_file_and_validate)
validate_button.pack(pady=10)

# Run the main event loop
root.mainloop()