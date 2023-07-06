from airflow import DAG
from airflow.operators.bash import BashOperator
import pendulum
import os


with DAG(
    dag_id="1_gas_bash",
    schedule="@daily",
    start_date=pendulum.datetime(2023,6,11,tz="UTC")#Task Start date
    ) as dag:

    gas = BashOperator(
        task_id ="gas",#task name
        bash_command='python  /opt/airflow/dags/scripts/gas.py'#Task execute
    )

    gas