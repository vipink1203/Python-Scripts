'''
Purpose: This script is used for get all the Databricks jobs which have not run for more than 15 Days
Author: vipink1203
website: https://www.vipinkumar.me
'''

from datetime import datetime, timedelta
import json
import requests
import tabulate

head = {'Authorization': 'Bearer <DatabricksToken>', 'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive', 'Content-Type': 'application/json', 'cache-control': 'no-cache'}


def getAllJobs():
    '''
    Getting all the job id's in a list
    '''
    url = 'https://<URL>/api/2.0/jobs/list'
    req = requests.get(url, headers=head)
    out = json.loads(req.content)
    job_ids = []
    for i in out['jobs']:
        job_ids.append(i['job_id'])

    return job_ids


def getEachJob(job_id):
    '''
    Making API request for each job id and converting the needed information into a list of dictionaries.
    '''
    jobs = []
    for jobid in job_id:
        url = 'https://<URL>/api/2.0/jobs/runs/list?job_id={}&active_only=false&offset=1&limit=1'.format(
            jobid)
        req = requests.get(url, headers=head)
        output = json.loads(req.content)
        if output.get('has_more'):
            for job_details in output['runs']:
                epoctime = int(str(job_details.get('start_time'))[:-3])
                delta = datetime.now() - \
                    datetime.fromtimestamp(
                        int(str(job_details.get('start_time'))[:-3]))
                job = {
                    'name': job_details.get('run_name'),
                    'job_id': jobid,
                    'run_date': datetime.fromtimestamp(epoctime).strftime('%Y-%m-%d'),
                    'last_run_diff': delta.days
                }
                jobs.append(job)
    print('Total of {} jobs were found!!!'.format(len(jobs)))
    result = [i for i in jobs if i.get('last_run_diff') >= 15]
    return result


def prettyDisplay(jobs):
    '''
    Using tablulate module to display the information we have in a nice table.
    '''
    dataset = jobs
    header = dataset[0].keys()
    rows = [x.values() for x in dataset]
    print(tabulate.tabulate(rows, header, tablefmt='grid'))


if __name__ == "__main__":
    job_ids = getAllJobs()
    jobs = getEachJob(job_ids)
    prettyDisplay(jobs)
