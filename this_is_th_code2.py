import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import PyPDF2

# Sample private key (replace this with your actual RSA private key data in PEM format)
SAMPLE_PRIVATE_KEY_DATA = b"""
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA2Heg6gTW/AwmaYX04ZQfCEZ2+4HUOTH9fmp7+upLoHu1IJ9W
Wvcg69lkCNPNRQaPwPpzW7U2zpIbjqakiQwdpFljCl4kn5RBjIjJ9NxBmqqGIhqW
5CiVLpoSLW59HVh4LQP5Xov53DZxKq8jbl4la4DE3YwUZh0peHSywFXi6T7RAxNu
FGUCeQetBLzD3RuGChlGHcyscWBJ1mBrUxDSNtOQK1mtqyJmd9CdvJV3nGOGTHPj
m9HX1GzhWxMGXSniwj2Bmf7AkkihlfWw5StCr8HKAkzQevGkhsdoRHeC7sx/X9wL
fpNfSl12V1vz+9VdGgme2XodiBMyK1z3lUPrbQIDAQABAoIBACbL+hk3WNi/zLqo
+aTciVtQVc7qDAFcRlS7/RCRoZBX27THGhEfrdTXl6hFXcr7TBSITtim9/W6FhpR
H7g4Za+pHakkCmhXiBAKDDhIqbFw0q2WGmk2JNa/YnamEOKLkq5uwekCKXwgfdPq
o+0KDqbf42jZzGYo39/o+oiiXBL1jLRY4w1ySuUZT9MrSEPqtUomGM7GcmXON8eV
1Xk8MHqJCcY82A9CuG5Npgoz4GV0imF6qRb9p+UJTswNpN+z1k0P3rTjdWS070ju
pXVW3NrJhEOhp1pe1qmbsZiZcWelLVgtsyY89wbh7CoSt70fO9rEgl2R09ewD/iX
UQhTpQECgYEA+cx2GMckgS99KhlztlaLyXF6GntvgZpA5TH2DmiqOQnGbMvQlLtN
PrwIz16spFcQ68EGA2eMuIPAuaaFOml46sP/hIs2OGBVLKo+Nr0J7CFgKCdXbI21
3lPuRtiUZpZkVx5eNitvUfxH9W/COa3w+OcwRJa3M1/NI4h0bGAgHA0CgYEA3ddW
Vt0cZ9gpKAZfsCGWYSu0mHUtlfoy1886hbxKZv0oPnU6ws1WJId4ukaA+4SuXN2H
XPbhSJRA14PPuiNczDW6REQiDu0Sn43Tq8L+/EpUk31Jc+E+BLIqLi/MZo3g1Z/i
GnVxcGMHnoumw9qTxgNUKZ0H15lNhLSfBE5zVOECgYAF/eWHSp+RibYS4HFqGkFY  
H6SyJevSzARqevxP9CrBG37q9SiXqLZ9nr0HXFn/xybcwNCIHF+/vUlOKrRfZlBE  
MVdbsosmZwkj/SFo5rfqNhK8Y9UxAWUvZAv/HwrQOyNFA7F20yvkZ4zCUl/ySj3R  
epopywOx88ZT594DC3s5sQKBgQCuroJw8bkNWBvIRYSRd1EngLe7GQHlR9dDMg1e  
A07+27cVv0+e1vtO1lHNM/kalHaL73BIVqo8cWjBiyxF4NSQhHoAiTncUPdKJe6Y  
IHqSBKGmZZAyLBmerwAh0Ed+NZfl/viWZwYFPiVgxYxySin0UOizv8/OCAwPQ/62  
8GNGYQKBgQDYYoOsDUH04qIFdN+T5DdEn9htwh30xrCGKn79I5Av+tb22dDRv2Ca  
Ky8a14J17fUOQaBh13PfDH3LL4eXpce7EGOV4uctrecxlvqsYQP2YFstWan+0ynP  
kIjFTUSJrx/DjwH63Omu2RK7WjYINnQew0wSxy43nB6VjLCRDYU7jA==
-----END RSA PRIVATE KEY-----
"""

def sign_document(file_path):
    try:
        # Load the RSA private key from PEM format
        private_key = serialization.load_pem_private_key(
            SAMPLE_PRIVATE_KEY_DATA,
            password=None,  # Assuming no password protection
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

        # Generate QR code with document details
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(f"Signed Document: {os.path.basename(signed_file_path)}")
        qr.make(fit=True)

        # Create QR code image
        qr_image = qr.make_image(fill_color="black", back_color="white")

        # Embed QR code in the corner of the signed PDF document
        embed_qr_code(signed_file_path, qr_image)

        messagebox.showinfo("Success", f"Document signed successfully.\nSigned file saved as: {signed_file_path}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to sign document: {e}")

def embed_qr_code(signed_file_path, qr_image):
    # Create a new PDF file to embed the QR code
    output_file_path = signed_file_path[:-4] + "_qr_embedded.pdf"

    # Open the existing signed PDF file
    existing_pdf = PyPDF2.PdfFileReader(open(signed_file_path, "rb"))

    # Create a new PDF canvas to draw the QR code
    c = canvas.Canvas(output_file_path, pagesize=letter)
    qr_image_path = "temp_qr_code.png"
    qr_image.save(qr_image_path)

    # Draw the QR code image at the desired position (e.g., bottom-left corner)
    c.drawInlineImage(qr_image_path, 50, 50, width=100, height=100)
    c.save()

    # Merge the signed PDF document with the PDF containing the embedded QR code
    output_pdf = PyPDF2.PdfFileReader(open(output_file_path, "rb"))
    combined_pdf = PyPDF2.PdfFileWriter()

    for i in range(min(existing_pdf.getNumPages(), output_pdf.getNumPages())):
        existing_page = existing_pdf.getPage(i)
        output_page = output_pdf.getPage(i)
        existing_page.merge_page(output_page)
        combined_pdf.addPage(existing_page)

    # Save the combined PDF document
    with open(signed_file_path, "wb") as merged_file:
        combined_pdf.write(merged_file)

    # Clean up temporary files
    os.remove(output_file_path)
    os.remove(qr_image_path)

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
