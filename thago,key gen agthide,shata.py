import tkinter as tk
from tkinter import messagebox
import mysql.connector
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding

def generate_rsa_key_pair():
    # Generate RSA private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,  # Recommended value for RSA
        key_size=2048           # Key size (bits)
    )

    # Get the corresponding public key
    public_key = private_key.public_key()

    # Serialize private key to PEM format
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Serialize public key to PEM format
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_key_pem, public_key_pem

def save_keys_to_database(private_key_pem, public_key_pem):
    try:
        # Connect to MySQL database
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_password',
            database='loginsystem'
        )
        cursor = conn.cursor()

        # Insert private and public keys into database
        cursor.execute("INSERT INTO pkey (private_key, public_key) VALUES (%s, %s)",
                       (private_key_pem, public_key_pem))
        conn.commit()

        messagebox.showinfo("Success", "RSA key pair generated and stored in database.")

    except mysql.connector.Error as error:
        messagebox.showerror("Error", f"Failed to store RSA keys in database: {error}")

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

def generate_and_store_keys():
    # Generate RSA key pair
    private_key_pem, public_key_pem = generate_rsa_key_pair()

    # Store keys in MySQL database
    save_keys_to_database(private_key_pem, public_key_pem)

# Create the main window
root = tk.Tk()
root.title("RSA Key Pair Generator")

# Create a button to generate and store keys
generate_button = tk.Button(root, text="Generate RSA Key Pair", command=generate_and_store_keys)
generate_button.pack(pady=20)

# Run the main event loop
root.mainloop()
