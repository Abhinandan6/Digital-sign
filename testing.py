import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

# Sample private key (replace this with your actual RSA private key data in PEM format)
SAMPLE_PRIVATE_KEY_DATA = b"""
-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC3V2DUSFv4Pcbg
aS7QCdZwhGT5rTghI4qHl77sFHIyobjVt937FvlLe/JQSYf+RVe7varX6rYYco7v
uLagb83UBcPWTsVRayBGq/UtH1npFVRSIUD4erwsjG0qmtAUE/0CRyI+8rVo9ff0
uu2EpbDEGNRrY6GHlpEOlCWb9Ycq+2F0yyX3thLoHd8ZO0RNH5SE9i5LK0nvXD94
+uSubZeatl0VvzmKFtKlhbh9GLJhKMdzWJ0JTkhH3GVT7Vrb9TLNlBwuly3QQZp4
icVb4NqzARIAkBaLhbIVxT2ocQpKNQcF6t0UggyEsq1WUYpDAvSKeBGuFrGjD1+R
oqmjOiR5AgMBAAECggEAPKrHObdv52bZxixH90MqGDVXDF9LMXwHPPLzlD73wtVM
yjt7Uri5aUbsWbDbNUJQ06jhPW1HMDPIJH7kv5X/b+cwdFvAYz6lgX0pNfMn1z7d
lge27gH+/mbBQNXVgK9Ui0pqhJXffYnWsL6iFcCWC22D7L0dGDa0bTSMdVz7izbu
aFd3d/+js8xgL6FQViLcAllyasCLvW+kFbr3JnCZ/+wdhww7TyHnwR9a1rK21pZG
RV/zkSJhmZnSPcokQgqUP8P1KQVYcEQ+5JNPprIiEMl4UNbeGpCodlLyFnBH42cd
jf9KFg9sxXSG5X5Gx2fMYaWXtrnKyFtJWUGRBcojeQKBgQD8nOiAWJuXuQhg1ygS
9ToXMYfr2Z4ZIm8k1qJGMnnvgEvDBwocPuHNghQbN1c4UFvWDc3S+0bdf8wbHCXm
woAXFv3bhWq3L9cOPifSY08jYPmv8vVCKti6OCJaa1YWxfXXaa55zOEz1kFJF04V
5h13S3v/I4vp+2mwFpt8sOO+XwKBgQC5zLIhmjQBvgQj51lKVDL/nRNmfkQKverw
BqzNBqNa2JdZQjoIaB1aSVkPivYJmOW5F3ZVCETROWWkDrGXIlMncXSM9LH1gn6g
PUjBP7UxRvwnx98S+UGURLklkMwdVUZ4VrICpyiv04S5Sb33zUWVT5UkRK/UTtOi
KIZhoKJcJwKBgHlKMYxmfxajXjV5OSGZIzI9swB4NaPl1629bJ7933Qyiq3ytFUJ
kEunWFYVBUjhtKabbCcQRV9W3D5sDnq1CuGLRYpgjfO1AbIx/9bRng7joh9sLXx+
rB8FkuENRoGavUaX1JFg4QSNrD0W9oQnQCCmWrwPaj+HWqCUykVdfYxLAoGBALjG
sYBpcr8o0cVDFrGs+urqs5iCifiE11jNypw7tclrDVlfW4dww4A+4atrbzQsMonY
o339MzM/+a0mT8cWA8x+MILd9v1KQdPqHqjRSsku5yZIx7h+2pExp0+MqPGjFOoo
je/Ffdkeaig7Bgmiw0iyVIg1JwflPONPmhUNQ2qRAoGAV8uJMU2J/Z4HLhlbrfl1
xAbHbJZt2iwJD5E2jpb8EfgR9hVXDN6qTAaZlZC5UPYSHtLGBGYwu7jH4K+ktB79
GjNS2Vi67QEprnkWk5Wqli7Fbmd8j52uEac8hNUFwYK9DSjtrrbOcRHh1gMbiDUr
pOMbW70lQAAA1PaqFfN3ddw=
-----END PRIVATE KEY-----
"""

# sample public key
SAMPLE_PUBLIC_KEY=b"""
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAt1dg1Ehb+D3G4Gku0AnW
cIRk+a04ISOKh5e+7BRyMqG41bfd+xb5S3vyUEmH/kVXu72q1+q2GHKO77i2oG/N
1AXD1k7FUWsgRqv1LR9Z6RVUUiFA+Hq8LIxtKprQFBP9AkciPvK1aPX39LrthKWw
xBjUa2Ohh5aRDpQlm/WHKvthdMsl97YS6B3fGTtETR+UhPYuSytJ71w/ePrkrm2X
mrZdFb85ihbSpYW4fRiyYSjHc1idCU5IR9xlU+1a2/UyzZQcLpct0EGaeInFW+Da
swESAJAWi4WyFcU9qHEKSjUHBerdFIIMhLKtVlGKQwL0ingRrhaxow9fkaKpozok
eQIDAQAB
-----END PUBLIC KEY-----
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

def browse_file_and_sign():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
    if file_path:
        sign_document(file_path)

def browse_file_and_validate():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
    if file_path:
        validate_signed_document(file_path, SAMPLE_PUBLIC_KEY)

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
