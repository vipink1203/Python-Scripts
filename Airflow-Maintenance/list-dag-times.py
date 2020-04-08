import psycopg2
from airflow.hooks.base_hook import BaseHook

connection = BaseHook.get_connection("airflow_db")
user = connection.login
password = connection.password
host = connection.host
port = connection.port
database = connection.schema

try:
    connection = psycopg2.connect(user=user, password=password, host=host, port=port, database=database)
    cursor = connection.cursor()
    postgreSQL_select_Query = "SELECT dag_id, AVG(DATE_PART('hour', end_date - start_date) + DATE_PART('minute', end_date - start_date) / 60) as dag_run_time_hours, DATE_PART('hour', MAX(execution_date)) || ':' || DATE_PART('minute', MAX(execution_date)) as dag_scheduled_time_est from dag_run where end_date > '2020-01-01' and state = 'success' group by dag_id"
    cursor.execute(postgreSQL_select_Query)
    dag_records = cursor.fetchall()
    for row in dag_records:
        print("dag_id = ", row[0],)
        print("dag_run_time_hours = ", row[1])
        print("dag_scheduled_time_est  = ", row[2], "\n")

except (Exception, psycopg2.Error) as error:
    print("Error while fetching data from PostgreSQL", error)

finally:
    # closing database connection.
    if(connection):
        cursor.close()
        connection.close()
