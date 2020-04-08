import psycopg2
import sys
from datetime import date
from airflow.hooks.base_hook import BaseHook

today = date.today()
connection = BaseHook.get_connection("airflow_db")
user = connection.login
password = connection.password
host = connection.host
port = connection.port
database = connection.schema
notSuccessQuery = """select t.dag_id
from task_instance t, dag_run d
where t.dag_id = d.dag_id and t.execution_date::date = d.execution_date::date
and d.end_date::date = '{}'
and t.state != 'success'
group by t.dag_id""".format(today)

blankQuery = """with task_count (dag_id, tasks) as
(select dag_id, max(tasks) tasks
from
(
select dag_id, count(distinct task_id) tasks
from
task_instance
where start_date::date >= now()::date - 7
group by dag_id
) s
group by s.dag_id
)

select t.dag_id --, count(task_id) todays_task_instances, max(tasks) total_tasks
from task_instance t, task_count c, dag_run d
where t.dag_id = c.dag_id and t.dag_id = d.dag_id and t.execution_date::date = d.execution_date::date
and d.end_date::date = '{}'
group by t.dag_id
having count(t.task_id) < max(tasks)""".format(today)
queries = [notSuccessQuery, blankQuery]
result = []


def clearDagState(clearItems):
    """
    Restart the scheduler and clear the dag error state
    """
    print('Restarting Scheduler Service')
    for dag in clearItems:
        print('clearing airflow state for {}'.format(dag))


def removeDuplicateDags(items):
    """
    Remove duplicate dags from the list if any
    """
    seen = set()
    res = []
    for item in items:
        if item not in seen:
            seen.add(item)
            res.append(item)
    return res


def executeQuery(query):
    """
    connecting to DB and execute query
    """
    try:
        connection = psycopg2.connect(user=user, password=password, host=host, port=port, database=database)
        cursor = connection.cursor()
        postgreSQL_select_Query = query
        cursor.execute(postgreSQL_select_Query)
        dag_id = cursor.fetchall()
        for dags in dag_id:
            for dag in range(0, len(dags)):
                result.append(dags[dag])

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()


if __name__ == "__main__":
    """
    - Call the executeQuery function for each queries
    - Check if the length of the result is not zero else remove the duplicates if any
    - Call clearDagState to rerun the errored dags.
    """
    for query in queries:
        executeQuery(query)
    if len(result) != 0:
        issueDagsList = removeDuplicateDags(result)
    else:
        print('No issue with the dags on {}!!'.format(today))
        sys.exit(0)
    clearDagState(issueDagsList)
