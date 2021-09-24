"""
The aim of this script is to decrypt the encrypted file using KMS key.
Author: Vipin Kumar V
Website: https://www.vipinkumar.me/
"""

import boto3

kms = boto3.client('kms')


def decrypt_key():
    """Decrypting the encrypted file"""

    with open("EncryptedFile", "rb") as f:
        byte = f.read()
        resp = kms.decrypt(CiphertextBlob=byte)
        f.close()
    plainKey = resp['Plaintext']
    final_key = plainKey.decode('UTF-8')
    return final_key


ssh_key = decrypt_key()
print(ssh_key)
