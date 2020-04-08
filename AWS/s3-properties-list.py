"""
The aim of this script is to list AWS S3 bucket properties such as
- Server Logging
- Versioning
- Default Encryption

Author: Vipin Kumar V
Website: https://www.vipinkumar.me/
"""

import boto3

client = boto3.client('s3')


class bcolors:
    HEADER = '\033[95m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


response1 = client.list_buckets()

print(bcolors.HEADER + 20*'*' + 'Checking S3 Bucket Logging' + 20*'*' + bcolors.ENDC)
for i in range(len(response1['Buckets'])):
    name = response1['Buckets'][i]['Name']
    try:
        logging = client.get_bucket_logging(Bucket=name)
        p = logging[u'LoggingEnabled']
        if p is not None:
            print(bcolors.OKGREEN + 'Enabled: ' + name + bcolors.ENDC)
    except Exception:
        print(bcolors.FAIL + 'Disabled: ' + name + bcolors.ENDC)

print('\n' + bcolors.HEADER + 20*'*' + 'Checking S3 Default Encryption' + 20*'*' + bcolors.ENDC)
for i in range(len(response1['Buckets'])):
    name = response1['Buckets'][i]['Name']
    try:
        response2 = client.get_bucket_encryption(Bucket=name)
        p = response2[u'ServerSideEncryptionConfiguration']
        if p is not None:
            print(bcolors.OKGREEN + 'Enabled: ' + name + bcolors.ENDC)
    except Exception:
        print(bcolors.FAIL + 'Disabled: ' + name + bcolors.ENDC)

print('\n' + bcolors.HEADER + 20*'*' + 'Checking S3 Bucket Versioning' + 20*'*' + bcolors.ENDC)
for i in range(len(response1['Buckets'])):
    name = response1['Buckets'][i]['Name']
    bucket_versioning = client.get_bucket_versioning(Bucket=name)
    p = bucket_versioning[u'Status']
    if p == 'Enabled':
        print(bcolors.OKGREEN + 'Enabled: ' + name + bcolors.ENDC)
    else:
        print(bcolors.FAIL + 'Disabled: ' + name + bcolors.ENDC)
