import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import mysql.connector
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import qrcode
import datetime

# MySQL Database Connection
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin123",
    database="key_management"
)

def retrieve_private_key(username, password):
    try:
        cursor = db_connection.cursor()
        query = "SELECT private_key FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        row = cursor.fetchone()
        cursor.close()

        if row:
            private_key_bytes = row[0]
            private_key = serialization.load_pem_private_key(private_key_bytes, password=None)
            return private_key
        else:
            return None
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Failed to retrieve private key: {err}")
        return None

def sign_document(file_path, private_key, username):
    try:
        with open(file_path, "rb") as file:
            document_data = file.read()

        hash_algorithm = hashes.SHA256()
        hash_value = hashes.Hash(hash_algorithm)
        hash_value.update(document_data)
        digest = hash_value.finalize()

        signature = private_key.sign(
            digest,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            algorithm=hash_algorithm
        )

        signed_file_path = file_path[:-4] + "_signed.pdf"
        with open(signed_file_path, "wb") as signed_file:
            signed_file.write(document_data)
            signed_file.write(signature)

        embed_qr_code(signed_file_path, username)
        messagebox.showinfo("Success", f"Document signed and saved as {signed_file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to sign document: {e}")

def embed_qr_code(signed_file_path, username):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(f"Username: {username}\nTimestamp: {datetime.datetime.now()}")
    qr.make(fit=True)

    qr_image = qr.make_image(fill_color="black", back_color="white")

    # Embed QR code into the signed PDF document
    output_file_path = signed_file_path[:-4] + "_qr_embedded.pdf"
    c = canvas.Canvas(output_file_path, pagesize=letter)
    c.setPageSize((792, 612))  # Letter size in points (8.5 x 11 inches)

    # Draw the QR code at the bottom-right corner
    qr_width, qr_height = qr_image.size
    c.drawInlineImage(qr_image, 500 - qr_width, 100, width=qr_width, height=qr_height)

    # Add the original signed pages to the output PDF
    input_pdf = canvas.Canvas(signed_file_path)
    num_pages = input_pdf.getNumPages()
    for page_num in range(num_pages):
        input_pdf.showPage()
        c.showPage()

    c.save()

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
    if file_path:
        username = simpledialog.askstring("Username", "Enter your username:")
        password = simpledialog.askstring("Password", "Enter your password:", show='*')

        if username and password:
            private_key = retrieve_private_key(username, password)
            if private_key:
                sign_document(file_path, private_key, username)
            else:
                messagebox.showerror("Error", "Invalid username or password")

# Create the main window
root = tk.Tk()
root.title("Document Signer")
root.geometry("600x400")
root.configure(bg="#87CEEB")

# Create a button to browse and sign a document
browse_button = tk.Button(root, text="Browse Document and Sign", command=browse_file, bg="white", fg="black", font=("Arial", 14))
browse_button.pack(pady=50)

# Run the main event loop
root.mainloop()

# Close the database connection when the application exits
db_connection.close()
