"""
Purpose: To find out the inactive users in slack. By default you are seeing the list of users who has inactivity of 14 days and above. 
This could narrow down your search.

Author: Vipin Kumar V
Website: https://www.vipinkumar.me/
"""

import json
import requests
import time
import sys

class bcolors:
    HEADER = '\033[95m'
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    WARNING = '\033[93m'


print(bcolors.WARNING + 'WARNING: This script finds only inactive users reported by slack due to 14 days of inactivity' + bcolors.ENDC)
time.sleep(5)
url='https://slack.com/api/team.billableInfo'
head = {'Authorization': 'Bearer <Add slack API token here>','Accept': '*/*','Accept-Encoding': 'gzip, deflate','Connection': 'keep-alive','Content-Type': 'application/x-www-form-urlencoded'}


req = requests.get(url, headers=head)
out = json.loads(req.content)
billable_info = out['billable_info']
userids = []
inactive_users = []
[userids.append(key) for key in billable_info]
for user in userids:
    if not billable_info[user]['billing_active']:
        inactive_users.append(user)
    else:
        pass

app_users = ['polly', 'push', 'jirabot', 'googledrive', 'devops191', 'github', 'outlook_calendar',
            'pullreminders', 'gif_keyboard', 'confluence']
if len(inactive_users) != 0:
    print(bcolors.FAIL + 20*'*' + 'Inactive Users Found: ' + 20*'*' + bcolors.ENDC)
    time.sleep(2.4)
else:
    print(bcolors.OKGREEN + 'All good!!! No inactive users were found.' + bcolors.ENDC)
    sys.exit(0)
    
for inact in inactive_users:
    url2 = 'https://slack.com/api/users.info' + str('?') + str('user=') + str(inact)
    url2res = requests.get(url2, headers=head)
    out2 = json.loads(url2res.content)
    userinfo = out2['user']
    if userinfo['name'] not in app_users:
        print(userinfo['name'])