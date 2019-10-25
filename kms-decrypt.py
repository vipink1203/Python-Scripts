import base64
import boto3

kms = boto3.client('kms')
def decrypt_key():
    with open("EncryptedFile", "rb") as f:
        byte = f.read()
        resp = kms.decrypt(CiphertextBlob=byte)
        plainKey = resp['Plaintext']
        final_key = plainKey.decode('UTF-8')
        return final_key

ssh_key = decrypt_key()
print(ssh_key)