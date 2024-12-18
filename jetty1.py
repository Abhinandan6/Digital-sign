import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader  # Import ImageReader from reportlab

import qrcode
import io  # Import the io module for BytesIO

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

        # Write the signed document with signature to the output file
        with open(signed_file_path, "wb") as signed_file:
            signed_file.write(document_data)
            signed_file.write(signature)

        # Embed QR code, signer text, and timestamp at the end of the signed PDF
        embed_qr_code(signed_file_path, "John Doe", "2024-05-09")

        messagebox.showinfo("Success", f"Document signed and saved as {signed_file_path}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to sign document: {e}")

def embed_qr_code(signed_file_path, signer_name, timestamp):
    try:
        # Generate QR code with signer and timestamp details
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(f"Signer: {signer_name}\nTimestamp: {timestamp}")
        qr.make(fit=True)

        # Create QR code image as PIL Image
        img = qr.make_image(fill_color="black", back_color="white")

        # Open the signed PDF document using PyPDF2
        existing_pdf = PdfReader(signed_file_path)
        output_pdf = PdfWriter()

        # Iterate over each page and embed QR code, signer text, and timestamp
        for page in existing_pdf.pages:
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)

            # Draw QR code image on the canvas
            qr_image = can.drawInlineImage(img, x=100, y=100, width=100, height=100)
            
            # Draw signer name dynamically
            can.drawString(100, 80, f"Signer: {signer_name}")
            can.drawString(100, 60, f"Timestamp: {timestamp}")

            # Save the canvas content
            can.save()

            # Move to the beginning of the StringIO buffer
            packet.seek(0)
            new_page = PdfReader(packet).pages[0]
            page.merge_page(new_page)
            output_pdf.add_page(page)

        # Write the modified PDF with embedded QR code, signer text, and timestamp
        with open(signed_file_path, "wb") as output_file:
            output_pdf.write(output_file)

        messagebox.showinfo("Success", f"QR code and text embedded in PDF: {signed_file_path}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to embed QR code and text: {e}")    
    try:
        # Generate QR code with signer and timestamp details
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(f"Signer: {signer_name}\nTimestamp: {timestamp}")
        qr.make(fit=True)

        # Create QR code image as PIL Image
        img = qr.make_image(fill_color="black", back_color="white")

        # Open the signed PDF document using PyPDF2
        existing_pdf = PdfReader(signed_file_path)
        output_pdf = PdfWriter()

        # Iterate over each page and embed QR code, signer text, and timestamp
        for page in existing_pdf.pages:
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)

            # Draw QR code image on the canvas
            qr_image = can.drawInlineImage(img, x=100, y=100, width=100, height=100)
            
            # Draw signer name and timestamp
            can.drawString(100, 80, f"Signer: {signer_name}")
            can.drawString(100, 60, f"Timestamp: {timestamp}")

            # Save the canvas content
            can.save()

            # Move to the beginning of the StringIO buffer
            packet.seek(0)
            new_page = PdfReader(packet).pages[0]
            page.merge_page(new_page)
            output_pdf.add_page(page)

        # Write the modified PDF with embedded QR code, signer text, and timestamp
        with open(signed_file_path, "wb") as output_file:
            output_pdf.write(output_file)

        messagebox.showinfo("Success", f"QR code and text embedded in PDF: {signed_file_path}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to embed QR code and text: {e}")    
    try:
        # Generate QR code with signer and timestamp details
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(f"Signer: {signer_name}\nTimestamp: {timestamp}")
        qr.make(fit=True)

        # Create QR code image as PIL Image
        img = qr.make_image(fill_color="black", back_color="white")

        # Open the signed PDF document using PyPDF2
        existing_pdf = PdfReader(signed_file_path)
        output_pdf = PdfWriter()

        # Iterate over each page and embed QR code, signer text, and timestamp
        for page in existing_pdf.pages:
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)
            
            # Convert PIL Image to reportlab-compatible format
            img_temp = io.BytesIO()
            img.save(img_temp, format='PNG')  # Save PIL Image to bytes
            img_temp.seek(0)  # Reset the file pointer

            # Draw QR code image on the canvas
            can.drawInlineImage(ImageReader(img_temp), x=100, y=100, width=100, height=100)
            can.drawString(100, 80, f"Signer: {signer_name}")
            can.drawString(100, 60, f"Timestamp: {timestamp}")
            can.save()

            # Move to the beginning of the StringIO buffer
            packet.seek(0)
            new_page = PdfReader(packet).pages[0]
            page.merge_page(new_page)
            output_pdf.add_page(page)

        # Write the modified PDF with embedded QR code, signer text, and timestamp
        with open(signed_file_path, "wb") as output_file:
            output_pdf.write(output_file)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to embed QR code and text: {e}")
    try:
        # Generate QR code with signer and timestamp details
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(f"Signer: {signer_name}\nTimestamp: {timestamp}")
        qr.make(fit=True)

        # Create QR code image as PIL Image
        img = qr.make_image(fill_color="black", back_color="white")

        # Open the signed PDF document using PyPDF2
        existing_pdf = PdfReader(signed_file_path)
        output_pdf = PdfWriter()

        # Iterate over each page and embed QR code, signer text, and timestamp
        for page in existing_pdf.pages:
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)
            can.drawInlineImage(ImageReader(img), x=100, y=100, width=100, height=100)
            can.drawString(100, 80, f"Signer: {signer_name}")
            can.drawString(100, 60, f"Timestamp: {timestamp}")
            can.save()

            # Move to the beginning of the StringIO buffer
            packet.seek(0)
            new_page = PdfReader(packet).pages[0]
            page.merge_page(new_page)
            output_pdf.add_page(page)

        # Write the modified PDF with embedded QR code, signer text, and timestamp
        with open(signed_file_path, "wb") as output_file:
            output_pdf.write(output_file)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to embed QR code and text: {e}")

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
    if file_path:
        sign_document(file_path)

# Create the main window
root = tk.Tk()
root.title("Document Signer")

# Create a button to browse and sign a document
browse_button = tk.Button(root, text="Browse Document and Sign", command=browse_file)
browse_button.pack(pady=20)

# Run the main event loop
root.mainloop()
