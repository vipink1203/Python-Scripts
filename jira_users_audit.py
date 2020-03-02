"""
Purpose: The aim of this script is to get the exported users csv file from JIRA and provide a final
        report on users who have not logged in for more than 3 months.
Author: Vipin Kumar V
Website: https://www.vipinkumar.me/
"""
# coding: utf-8

import sys
import pandas as pd
import numpy as np
import datetime
import xlsxwriter
pd.options.mode.chained_assignment = None

def pd_works():
    filename = input('Please enter the path to the csv file exported from JIRA: ')
    df = pd.read_csv(filename)
    df = df.drop(columns=['id', 'created', 'Last seen in Jira Service Desk', 'Last seen in Confluence'])
    df.rename(columns = {'Last seen in Jira Software':'last_seen_jira'}, inplace = True)
    df_n_logon = df[(df['last_seen_jira'] == 'Never logged in')]
    df_wo_nev = df.loc[(df['last_seen_jira'] != 'Never logged in')]
    df_wo_nev['last_seen_jira'] = pd.to_datetime(df_wo_nev['last_seen_jira'])
    df_wo_nev['current_date'] = pd.datetime.now().date()
    df_wo_nev['current_date'] = df_wo_nev['current_date'].values.astype('datetime64[D]')
    df_wo_nev['jira_months'] = ((df_wo_nev['current_date'] - df_wo_nev['last_seen_jira'])/np.timedelta64(1, 'M')).astype(int)
    df_months = df_wo_nev.loc[(df_wo_nev['jira_months'] >= 3)]
    df_months = df_months.drop(columns=['current_date'])
    exceptions = ['devsecops-wrike@aetnd.com', 'devops@aenetworks.com', 'jiradigital@aenetworks.com', 'cs-support@aenetworks.com',
                'devops-evident@aetnd.com', 'cw_aenetworks@contentwise.tv', 'international@aenetworks.legal',
                'technology@aenetworks.legal', 'corporate@aenetworks.legal', 'devsecops-centrify@aetnd.com', 
                'mobile-integrations@aenetworks.com']
    df_months = df_months[(~df_months['email'].isin(exceptions))]
    never_exceptions = ['contentservicesteam@aenetworks.com', 'cssupport@aetndigital.com',
                    'devops-support@aenetworks.com', 'devsecops-sf@aetnd.com', 'devops-redscout@aetv.com', 
                    'devops-tvgla@aetv.com', 'SVODesign@aenetworks.com']
    df_n_logon = df_n_logon[(~df_n_logon['email'].isin(never_exceptions))]

## Writing the final output
    path = r"./jira_audit_report.xlsx"
    writer = pd.ExcelWriter(path, engine = 'xlsxwriter')
    with pd.ExcelWriter(path) as writer:
        df_months.to_excel(writer, sheet_name='Inactive_Users', index=False)
        df_n_logon.to_excel(writer, sheet_name='Never_Logged_In_Users', index=False)
        writer.save()
        writer.close()

if __name__ == "__main__":
    pd_works()
    print('Your file is ready in the current directory named as jira_audit_report.xlsx')