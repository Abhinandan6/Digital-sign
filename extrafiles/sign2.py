import sys
import os
import hashlib
from datetime import datetime
import qrcode
from PyPDF2 import PdfReader, PdfWriter
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend

def sign_pdf(fname, lname, publicKeyPath, privateKeyPath, pdfFilePath):
    # Hashing
    hasher = hashlib.sha256()

    # Embedding user info and timestamp
    data = f"{fname} {lname} {datetime.now()}".encode()
    hasher.update(data)
    signature = hasher.digest()

    # Load RSA keys from files
    with open(privateKeyPath, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )

    with open(publicKeyPath, 'rb') as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )

    # RSA Encryption
    encrypted_signature = private_key.sign(
        signature,
        padding.PSS(
            mgf=padding.MGF1(hashlib.sha256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashlib.sha256()
    )

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(encrypted_signature)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Add QR code to PDF directly
    pdf = PdfReader(pdfFilePath)
    writer = PdfWriter()

    # Add pages
    for page in pdf.pages:
        writer.add_page(page)

    # Add QR code to the last page of the PDF
    last_page = pdf.pages[-1]
    last_page_width = last_page.mediaBox.getUpperRight_x()
    last_page_height = last_page.mediaBox.getUpperRight_y()

    # Adjust QR code position
    qr_x = last_page_width - 120  # Adjust this value as needed
    qr_y = last_page_height - 120  # Adjust this value as needed

    writer.add_inline_image(qr_img.tobytes(), qr_x, qr_y)

    # Write signed PDF
    signed_pdf_path = os.path.splitext(pdfFilePath)[0] + "_signed.pdf"
    with open(signed_pdf_path, "wb") as f_out:
        writer.write(f_out)

    return "PDF signed successfully"

if __name__ == "__main__":
    fname = sys.argv[1]
    lname = sys.argv[2]
    publicKeyPath = sys.argv[3]
    privateKeyPath = sys.argv[4]
    pdfFilePath = sys.argv[5]

    result = sign_pdf(fname, lname, publicKeyPath, privateKeyPath, pdfFilePath)
    print(result)
