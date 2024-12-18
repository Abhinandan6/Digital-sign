import qrcode
import hashlib
import PyPDF2
from Crypto.Signature import pkcs1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import pymysql
import sys
import datetime
import os

# Connect to MySQL database
def connect_to_database():
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='',
                                     db='loginsystem')
        return connection
    except pymysql.Error as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)

# Fetch user details from database
def fetch_user_details(cursor, user_id):
    sql = "SELECT firstname, lastname FROM users WHERE id = %s"
    cursor.execute(sql, (user_id,))
    result = cursor.fetchone()
    return result['firstname'], result['lastname']

# Fetch private key from database
def fetch_private_key(cursor, user_id):
    sql = "SELECT private_key FROM pkeys WHERE user_id = %s"
    cursor.execute(sql, (user_id,))
    result = cursor.fetchone()
    private_key_blob = result['private_key']
    return RSA.import_key(private_key_blob)

# Sign PDF
def sign_pdf(pdf_path, user_id, connection):
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)
            pdf_writer = PyPDF2.PdfFileWriter()

            connection = connect_to_database()
            with connection.cursor() as cursor:
                first_name, last_name = fetch_user_details(cursor, user_id)
                private_key = fetch_private_key(cursor, user_id)

                # Calculate PDF hash
                hash = hashlib.sha256()
                pdf_file.seek(0)
                hash.update(pdf_file.read())

                # Embed QR code
                qr_data = f"User ID: {user_id}, Name: {first_name} {last_name}, Timestamp: {datetime.datetime.now()}, Public Key: {private_key.publickey().export_key().decode('utf-8')}"
                qr = qrcode.make(qr_data)

                for page_num in range(pdf_reader.numPages):
                    page = pdf_reader.getPage(page_num)
                    pdf_writer.addPage(page)
                    if page_num == 0:
                        pdf_writer.addPage(qr)

                # Save signed PDF
                signed_pdf_path = os.path.join(os.path.dirname(pdf_path), f"signed_{os.path.basename(pdf_path)}")
                with open(signed_pdf_path, 'wb') as signed_pdf_file:
                    pdf_writer.write(signed_pdf_file)

                print("PDF signed successfully.")
                return signed_pdf_path
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    pdf_path = "example.pdf"  # Provide the path to your PDF
    user_id = 1  # Provide the user ID
    connection = None
    try:
        signed_pdf_path = sign_pdf(pdf_path, user_id, connection)
        if signed_pdf_path:
            print(f"Signed PDF saved at: {signed_pdf_path}")
    finally:
        if connection:
            connection.close()




























# import qrcode
# import hashlib
# import PyPDF2
# from Crypto.Signature import pkcs1_15
# from Crypto.Hash import SHA256
# from Crypto.PublicKey import RSA
# import pymysql
# import sys
# import datetime

# # Connect to MySQL database
# connection = pymysql.connect(host='localhost',
#                              user='root',
#                              password='',
#                              db='loginsystem')

# # Fetch user details from database
# def fetch_user_details(user_id):
#     with connection.cursor() as cursor:
#         sql = "SELECT firstname, lastname FROM users WHERE id = %s"
#         cursor.execute(sql, (user_id,))
#         result = cursor.fetchone()
#         return result['first_name'], result['last_name']

# # Fetch private key from database
# def fetch_private_key(user_id):
#     with connection.cursor() as cursor:
#         sql = "SELECT private_key FROM pkeys WHERE user_id = %s"
#         cursor.execute(sql, (user_id,))
#         result = cursor.fetchone()
#         private_key_blob = result['private_key']
#         return RSA.import_key(private_key_blob)

# def sign_pdf(pdf_path, user_id):
#     # Load PDF
#     pdf_file = open(pdf_path, 'rb')
#     pdf_reader = PyPDF2.PdfFileReader(pdf_file)
#     pdf_writer = PyPDF2.PdfFileWriter()

#     # Fetch user details
#     first_name, last_name = fetch_user_details(user_id)

#     # Fetch private key
#     private_key = fetch_private_key(user_id)

#     # Sign PDF
#     hash = hashlib.sha256()
#     hash.update(pdf_file.read())
#     pdf_file.close()

#     # Embed QR code
#     qr_data = f"User ID: {user_id}, Name: {first_name} {last_name}, Timestamp: {datetime.datetime.now()}, Public Key: {private_key.publickey().export_key().decode('utf-8')}"
#     qr = qrcode.make(qr_data)
#     qr.save("qr_code.png")

#     # Append QR code to PDF
#     pdf_writer.addPage(qr)
#     for page_num in range(pdf_reader.numPages):
#         page = pdf_reader.getPage(page_num)
#         pdf_writer.addPage(page)

#     # Save signed PDF
#     signed_pdf_path = f"signed_{pdf_path}"
#     with open(signed_pdf_path, 'wb') as signed_pdf_file:
#         pdf_writer.write(signed_pdf_file)

#     return signed_pdf_path

# if __name__ == "__main__":
#     pdf_path = sys.argv[1]
#     user_id = 1
#     signed_pdf_path = sign_pdf(pdf_path, user_id)
#     print(f"PDF signed and saved as: {signed_pdf_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sign_pdf.py <pdf_path>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    user_id = 1  # Change this to the actual user ID
    try:
        signed_pdf_path = sign_pdf(pdf_path, user_id)
        print(f"PDF signed and saved as: {signed_pdf_path}")
    except Exception as e:
        print(f"An error occurred: {e}")






# import qrcode
# import hashlib
# from PyPDF2 import PdfReader, PdfWriter
# from Crypto.Signature import pkcs1_15
# from Crypto.Hash import SHA256
# from Crypto.PublicKey import RSA
# import pymysql
# import sys
# import datetime

# # Connect to MySQL database
# connection = pymysql.connect(host='localhost',
#                              user='root',
#                              password='',
#                              db='loginsystem')

# # Fetch user details from database
# # Fetch user details from database
# def fetch_user_details(user_id):
#     with connection.cursor() as cursor:
#         sql = "SELECT fname, lname FROM users WHERE id = %s"
#         cursor.execute(sql, (user_id,))
#         result = cursor.fetchone()
#         return result['fname'], result['lname']


# # Fetch private key from database
# def fetch_private_key(user_id):
#     with connection.cursor() as cursor:
#         sql = "SELECT private_key FROM pkeys WHERE user_id = %s"
#         cursor.execute(sql, (user_id,))
#         result = cursor.fetchone()
#         private_key_blob = result['private_key']
#         return RSA.import_key(private_key_blob)

# def sign_pdf(pdf_path, user_id):
#     # Load PDF
#     pdf_reader = PdfReader(pdf_path)
#     pdf_writer = PdfWriter()

#     # Fetch user details
#     first_name, last_name = fetch_user_details(user_id)

#     # Fetch private key
#     private_key = fetch_private_key(user_id)

#     # Sign PDF
#     hash = hashlib.sha256()
#     with open(pdf_path, 'rb') as pdf_file:
#         hash.update(pdf_file.read())

#     # Embed QR code
#     qr_data = f"User ID: {user_id}, Name: {first_name} {last_name}, Timestamp: {datetime.datetime.now()}, Public Key: {private_key.publickey().export_key().decode('utf-8')}"
#     qr = qrcode.make(qr_data)
#     qr.save("qr_code.png")

#     # Append QR code to PDF
#     pdf_writer.add_page(qr)
#     for page in pdf_reader.pages:
#         pdf_writer.add_page(page)

#     # Save signed PDF
#     signed_pdf_path = f"signed_{pdf_path}"
#     with open(signed_pdf_path, 'wb') as signed_pdf_file:
#         pdf_writer.write(signed_pdf_file)

#     return signed_pdf_path

# if __name__ == "__main__":
#     if len(sys.argv) != 2:
#         print("Usage: python sign_pdf.py <pdf_path>")
#         sys.exit(1)

#     pdf_path = sys.argv[1]
#     user_id = 1  # Change this to the actual user ID
#     try:
#         signed_pdf_path = sign_pdf(pdf_path, user_id)
#         print(f"PDF signed and saved as: {signed_pdf_path}")
#     except Exception as e:
#         print(f"An error occurred: {e}")




# import qrcode
# import hashlib
# import PyPDF2
# from Crypto.Signature import pkcs1_15
# from Crypto.Hash import SHA256
# from Crypto.PublicKey import RSA
# import pymysql
# import sys
# import datetime

# # Connect to MySQL database
# def connect_to_database():
#     return pymysql.connect(host='localhost',
#                            user='root',
#                            password='',
#                            db='loginsystem',
#                            charset='utf8mb4',
#                            cursorclass=pymysql.cursors.DictCursor)

# # Fetch user details from database
# def fetch_user_details(connection, user_id):
#     with connection.cursor() as cursor:
#         sql = "SELECT fname, lname FROM users WHERE id = %s"
#         cursor.execute(sql, (user_id,))
#         result = cursor.fetchone()
#         if result:
#             return result['fname'], result['lname']
#         else:
#             return None, None

# # Fetch private key from database
# def fetch_private_key(connection, user_id):
#     with connection.cursor() as cursor:
#         sql = "SELECT private_key FROM pkey WHERE user_id = %s"
#         cursor.execute(sql, (user_id,))
#         result = cursor.fetchone()
#         if result:
#             private_key_blob = result['private_key']
#             return RSA.import_key(private_key_blob)
#         else:
#             return None

# def sign_pdf(pdf_path, user_id):
#     try:
#         connection = connect_to_database()

#         # Fetch user details
#         first_name, last_name = fetch_user_details(connection, user_id)
#         if not first_name or not last_name:
#             print("User not found or details incomplete.")
#             return

#         # Fetch private key
#         private_key = fetch_private_key(connection, user_id)
#         if not private_key:
#             print("Private key not found for the user.")
#             return

#         # Load PDF
#         with open(pdf_path, 'rb') as pdf_file:
#             pdf_reader = PyPDF2.PdfFileReader(pdf_file)
#             pdf_writer = PyPDF2.PdfFileWriter()

#             # Calculate PDF hash
#             pdf_hash = hashlib.sha256()
#             pdf_hash.update(pdf_file.read())
#             pdf_file.seek(0)

#             # Sign PDF hash
#             signer = pkcs1_15.new(private_key)
#             signature = signer.sign(pdf_hash.digest())

#             # Embed signature QR code into PDF
#             qr_data = f"User ID: {user_id}, Name: {first_name} {last_name}, Timestamp: {datetime.datetime.now()}, Signature: {signature.hex()}"
#             qr = qrcode.make(qr_data)
#             qr_bytes = qr.tobytes()

#             # Add signature as an attachment to PDF
#             pdf_writer.addAttachment("signature.qr", qr_bytes)

#             # Append PDF content
#             for page_num in range(pdf_reader.numPages):
#                 page = pdf_reader.getPage(page_num)
#                 pdf_writer.addPage(page)

#             # Save signed PDF
#             signed_pdf_path = f"signed_{pdf_path}"
#             with open(signed_pdf_path, 'wb') as signed_pdf_file:
#                 pdf_writer.write(signed_pdf_file)

#             print(f"PDF signed and saved as: {signed_pdf_path}")

#     finally:
#         if connection:
#             connection.close()

# if __name__ == "_main_":
#     if len(sys.argv) != 3:
#         print("Usage: python sign_pdf.py <pdf_path> <user_id>")
#         sys.exit(1)

#     pdf_path = sys.argv[1]
#     user_id = sys.argv[2]
#     sign_pdf(pdf_path, user_id)
