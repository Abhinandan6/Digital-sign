#!/usr/bin/env python3
import sys
import os
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

def load_public_key(public_key_path):
    with open(public_key_path, 'rb') as key_file:
        key_data = key_file.read()
        public_key = RSA.import_key(key_data)
        return public_key

def load_signature(signature_path):
    with open(signature_path, 'rb') as signature_file:
        signature_data = signature_file.read()
        return signature_data

def validate_signature(public_key, signature_data, pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_data = pdf_file.read()

    hash_object = SHA256.new(pdf_data)
    signature_object = PKCS1_v1_5.new(signature_data)

    try:
        signature_object.verify(public_key, hash_object)
        return True
    except:
        return False

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python sign_pdf_validator.py <public_key_path> <signature_path> <pdf_path>")
        sys.exit(1)

    public_key_path = sys.argv[1]
    signature_path = sys.argv[2]
    pdf_path = sys.argv[3]

    public_key = load_public_key(public_key_path)
    signature_data = load_signature(signature_path)

    if validate_signature(public_key, signature_data, pdf_path):
        print("Signature is valid.")
    else:
        print("Signature is invalid.")