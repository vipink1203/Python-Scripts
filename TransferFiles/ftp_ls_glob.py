'''
Purpose: The aim of this script is to use glob to search .py files and copy them from remote SFTP server to local PC.
Author: Vipin Kumar V
Website: https://www.vipinkumar.me/
'''

import paramiko
import time
import fnmatch

class bcolors:
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'

ip='10.0.0.41'
user='vkumar'
passwd='Password'
remote_path = '/Users/vkumar/Desktop/'
local_path = '/Users/vkumar/Desktop/python-workouts/'

print(bcolors.OKGREEN + '\nConnecting to FTP server. Please Wait...' + bcolors.ENDC)
time.sleep(4)
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=ip, username=user, password=passwd)
sftp = ssh_client.open_sftp()

print(bcolors.OKGREEN + 'Connected to FTP Server...' + bcolors.ENDC)
time.sleep(4)

print(bcolors.OKGREEN + 'Searching all .py files on FTP Server...' + bcolors.ENDC)
for filename in sftp.listdir(remote_path):
    if fnmatch.fnmatch(filename, '*.py'):
        file_remote = remote_path + filename
        file_local = local_path + filename
        sftp.get(file_remote, file_local)
print(bcolors.OKGREEN + 'Transfer Completed...' + bcolors.ENDC)
sftp.close()
ssh_client.close()