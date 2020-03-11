'''
Purpose: The aim of this script is to update the Travis-CI env variable which contains the github token. Can be used for other purposes as well.
Author: Vipin Kumar V
Website: https://www.vipinkumar.me/

How to Use?
Step 1: Config.ini file contains the travis and github token to make the API calls
Step 2: Search_str variable is used to search the .travis.yml file in every repositories to identify which repository uses Travis-CI
Step 3: The script will first delete the variable and then add the new token.
Step 4: Before running the script make sure you go through all the API calls and change the Github organisation name and env_name Variable.
'''

from configparser import ConfigParser
from github import Github
import requests
import json
import base64
import boto3

class bcolors:
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'

# Parsing the config file for all access
print(bcolors.OKGREEN + '\nStep 1. Parsing the config.ini file\n' + bcolors.ENDC)
configFilePath = './config.ini'
parser = ConfigParser()
parser.read(configFilePath)
g = Github(parser.get('GitHub', 'Token'))
org = g.get_organization('<org_name>')
travis_head = {'Authorization': parser.get('Travis', 'Token'), 'Accept': 'application/json', 'Travis-API-Version': '3'}

# Create a list with all the org repositories
print(bcolors.OKGREEN + 'Step 2. Getting list of all repositories from the organization\n' + bcolors.ENDC)
def org_all_repos():
    repo = org.get_repos()
    repos = [i.name for i in repo]
    return repos

current_repos = org_all_repos()

# search the string to identify the repos using Travis-CI
print(bcolors.OKGREEN + 'Step 3. Searching the string in .travis.yml file\n' + bcolors.ENDC)
search_str = parser.get('GitHub', 'search_str')
with_travis = []
for repository_name in current_repos:
    repo = org.get_repo(repository_name)
    try:
        file_contents = repo.get_contents('.travis.yml')
        contents = file_contents.decoded_content.decode('utf-8')
        if contents.find(search_str) != -1:
            with_travis.append(repository_name)
    except:
        pass

# Get all travis repos with travis specific IDs
print(bcolors.OKGREEN + 'Step 4. Making Travis API calls to get the repository IDs\n' + bcolors.ENDC)
travisRepoIds_list = []
def travisRepo_ids(val):
    url = 'https://api.travis-ci.com/owner/<org>/repos?offset=' + str(val)
    res = requests.get(url, headers=travis_head)
    j = json.loads(res.content)
    page = len(j['repositories'])
    count = j['@pagination']['count']
    for i in range(0, page):
        travisRepoIds_list.insert(i, j['repositories'][i])
    return count

count = 1
i = 0
while i < count:
    count = travisRepo_ids(i)
    i = i + 100

# Checking Travis repo list against the list 'with_travis'
print(bcolors.OKGREEN + 'Step 5. Checking Travis repo list against the list "with_travis"\n' + bcolors.ENDC)
for i in travisRepoIds_list:
    if i['name'] in with_travis:
        turl = 'https://api.travis-ci.com/repo/' + str(i['id']) + '/env_vars'
        tres = requests.get(turl, headers=travis_head)
        t = json.loads(tres.content)
        for j in t['env_vars']:
            if j['name'] == 'PUSH_TOKEN':
        
                # TO-DO: Update the token in place instead of deleting and adding
                # Delete the existing Token and add the new one
                durl = 'https://api.travis-ci.com/repo/' + str(i['id']) + '/env_var/' + str(j['id'])
                dres = requests.delete(durl, headers=travis_head)
                print(dres.status_code, ' - Token deleted - ', i['name'])
                
                # Adding the new Token
                uurl = 'https://api.travis-ci.com/repo/' + str(i['id']) + '/env_vars'
                uush_body = { "env_var.name": "PUSH_TOKEN", "env_var.value": parser.get('PUSH', 'Token') }
                ures = requests.post(uurl, headers=travis_head, data=uush_body)
                print(ures.status_code, ' - New Token Added - ', i['name'])