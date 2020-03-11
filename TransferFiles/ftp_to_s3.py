'''
Purpose: The aim of this simple script is to upload file from remote SFTP server to AWS S3 bucket.
Author: Vipin Kumar V
Website: https://www.vipinkumar.me/
'''
## TO-DO : - Multipart upload - Check if file already exists on S3
import paramiko
import boto3

class bcolors:
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'

s3_bucket = 'Test-Bucket'
s3_connection = boto3.client('s3')

ftp = '10.0.0.41'
user = 'vkumar'
passwd = 'password'
remote_path = '/Users/vkumar/Desktop/heartbeat.html'

print(bcolors.OKGREEN + '\nConnecting to FTP server. Please Wait...' + bcolors.ENDC)

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=ftp, username=user, password=passwd)
sftp = ssh_client.open_sftp()
print(bcolors.OKGREEN + 'Connected to FTP Server...' + bcolors.ENDC)
ftp_file = sftp.file(remote_path, 'r')
print(bcolors.OKGREEN + 'uploading file from FTP to ' + s3_bucket + ' bucket' + bcolors.ENDC)
s3_connection.upload_fileobj(ftp_file, s3_bucket, 'test/heartbeat.html')
print(bcolors.OKGREEN + 'Transfer completed. Closing Connections...' + bcolors.ENDC)
ftp_file.close()
ssh_client.close()