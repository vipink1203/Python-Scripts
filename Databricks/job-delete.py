'''
Purpose: This script is used for delete the Databricks jobs assuming that you have a txt file with all the job ids in each line
Author: @vipink1203
'''

import os
import json
import requests

TOKEN = os.environ.get('DATABRICKS_TOKEN')

head = {'Authorization': 'Bearer {}'.format(TOKEN), 'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive', 'Content-Type': 'application/json', 'cache-control': 'no-cache'}


def readDeleteJobs():
    with open('jobslist.txt') as f:
        to_delete = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    to_delete = [x.strip() for x in to_delete]
    f.close()
    return to_delete


def jobDelete(job_id):
    for id in job_id:
        url = 'https://<workspace-url>/api/2.0/jobs/delete'
        req = requests.post(url, headers=head, json={"job_id": id})
        print(req, 'Deleted id: ', id)


if __name__ == "__main__":
    to_delete = readDeleteJobs()
    jobDelete(to_delete)
