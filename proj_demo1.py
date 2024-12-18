import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

# Sample private key (replace this with your private key)
# Note: Keep your private key secure and do not hardcode it in production code
SAMPLE_PRIVATE_KEY = 'ABHI'

def sign_document(file_path):
    # Load the private key
    private_key = serialization.load_pem_private_key(
        SAMPLE_PRIVATE_KEY,
        password=None  # Assuming no password protection
    )

    try:
        # Read the document data
        with open(file_path, "rb") as file:
            document_data = file.read()

        # Compute SHA-256 hash of the document
        hash_value = hashes.Hash(hashes.SHA256())
        hash_value.update(document_data)
        digest = hash_value.finalize()

        # Sign the hash digest
        signature = private_key.sign(
            digest,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            )
        )

        # Write the signed document to a new file
        signed_file_path = file_path + ".signed"
        with open(signed_file_path, "wb") as signed_file:
            signed_file.write(document_data)
            signed_file.write(signature)

        messagebox.showinfo("Success", f"Document signed and saved as {signed_file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to sign document: {e}")

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
