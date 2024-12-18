import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

# Sample private key (replace this with your private key)
# Note: Keep your private key secure and do not hardcode it in production code
SAMPLE_PRIVATE_KEY = b"""-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAnR9hUkZCkHJhZkR7Up59cYhIZEcevltjCWBpjPyQrD2lftcm
9FTDycdjvKAYxKdmVx50NqoQanYmlwzeo/64sPuC2kdsBp+r70x8C3cNUzgbc5Qo
djjudO9ZkX98MLoiW1lPh+fq3INJUce/lBAW8I3YOSdeRc7byil2EPlXahN7nj/A
h9hqpYXuRKeTLWTSE5pd+cAsxlooSYtWAZpp/cmwOh3lFKFZK3Jq8kjsZuwPpnyu
hmqJnzTHTLP1IFgF6dczVeu4sIvTA2IhSOhK43Q/wfsd9NLjJrNpBpMIRt7jw0Ut
UYwG6UOVPb+p8QHQamt57EEInj9ufW3daoxlHwIDAQABAoIBACa2iiCe7hywCf6M
JgSTx123UfrfKRyG4M55IliaDD1cDRBFC7SMxBbN2W2q1p9xjX4uozyqx1Or29NA
2QR4KOJ2feWxTlUNd2wFINUkVrSn8N+X5CZI3bwTEzMNwbgxzHBMf5OBWXVOpbyQ
JkxhcH2BvYJLiGdT0gSsFYqWHOsmEc6Z6MA4L8K7qKC1F0nt3KZZJcF4xGPqd/tr
T2D/ACtU6t6AAeqyJS7ACfQrUmzBG/4+aN0wvVfy2vlxhYDbzPRr2DQsMYHz7Gf7
2F89+tyQsG2Jw2hK3sNGEOXgnBDoHYfA+5wb5LPureDFcFVWn70q09wbi5VR9khW
LcSDFakCgYEA0qDAvO6a2iTazsjL0bzFlycHjPaeeq6RfoUTq9faolnNVv36pfv3
LshZmq9w2kArbQqhDG0MhZvNipbOIzeJW4SEQpL/WXKFaYWU1LX0CIC0YVwGuje4
XiTEq5wMaPn8Ku9BejoniY0gLcM3kwpadUywNmFvv75xjElg1HUi/YkCgYEAvvgH
9Dnrk5x6NUj0x+6H5mVgBunWIWhlHEwj2T6A9NOiEtZTg8u3kmntKiYtB7nsVx+A
fNtYaSpwsfgCIsIMOJv1o3tIC0cqd0klt+MpPcF1pik7O78YxlbG87NZs4eS3f3e  
T3jmzamUCncD07tVch+V2SwBTY2iDdQQfU6Xi2cCgYAg63UUUmqre6UjOqj4f/uV  
80iv1H/ShuRAlQYNDrCiPUzlss5xEN+CVVgD4DXQNsVSxp2DNqwFWeOXLJjNUknK  
nvyY9yan0Ulew70OPd4FUjBfIyX+BuVu+WovtDUQVzn9b+WY9+vkCMWlwWQ3PCAF  
Q1YrObFgk6Bln7Zdnm04mQKBgAijBxkQlYrzhMNsLUXtj8/nvdQSN1EDe68v8l8c  
6JAqEiZv8w7+46qHh+ZkG51B12KJVjJPaUw4Uyh5Yv9Xb14QD6f5J2T7Lvx+HmqW  
p4LXgQ6mxrsJBYHS4uSas+/erdHEbY2Clk2u4bcnctDcpBypOQm9Z8GuKiod8TD5  
oPj5AoGBALcalw+/BjtenKhgn0lnYydr6+IGgrs0O5QOXlPHrTliRt58gtBIqnsI  
mQY1LrA4SadxZ8bExXLjK3iQxit/GhiM5poyz7p1PDCzn6BKvjwJ66mv/alMsl0q  
2JTMptH0jfw2xVFwBfN6cWHx6GYdf2wx9IrQrOAtGksrPbLl3COP
-----END RSA PRIVATE KEY-----"""

def sign_document(file_path):
    # Load the private key
    private_key = serialization.load_pem_private_key(
        SAMPLE_PRIVATE_KEY,
        password=None,  # Assuming no password protection
    )

    try:
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
