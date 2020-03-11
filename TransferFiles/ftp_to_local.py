import paramiko
 
ip='10.0.0.41'
user='vkumar'
passwd='Password'
files = ['index.html', 'examplefile']
remote_path = '/Users/vkumar/Desktop/'
local_path = '/tmp/'

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=ip, username=user, password=passwd)
sftp = ssh_client.open_sftp()

for lfile in files:
    file_remote = remote_path + lfile
    file_local = local_path + lfile

    print(file_remote + ' >>> ' + file_local)
    sftp.get(file_remote, file_local)

sftp.close()
ssh_client.close()