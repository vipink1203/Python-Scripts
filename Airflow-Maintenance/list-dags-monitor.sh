#!/bin/bash
## Since there is no direct way of getting the error from the 'airflow list_dags' command, this script is to identify that error and send it to respective SNS. 

runuser -l airflow -c 'airflow list_dags' > /tmp/list.txt 2>&1

if grep -q "ERROR" /tmp/list.txt;then
  message=`sed -n '1,/-----/ p' /tmp/list.txt`
  if [ $env == "prod" ];then
    aws sns publish --topic-arn arn:aws:sns:us-east-1:XXXXXXXXXXX:prod-sev --subject "Error found while listing airflow dags" --message "$message" --region us-east-1
  else
    aws sns publish --topic-arn arn:aws:sns:us-east-1:XXXXXXXXXXX:dev-sev --subject "Error found while listing airflow dags" --message "$message" --region us-east-1
  fi
fi