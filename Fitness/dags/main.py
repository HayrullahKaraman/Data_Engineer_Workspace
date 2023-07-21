from airflow import DAG
from airflow.operators.python import PythonOperator
import pendulum
from scripts.read_json import read_fitness
from scripts.save_cassandra import save_fitness
import os
import json
from cassandra.cluster import Cluster




with DAG(
    dag_id="Fitness",
    schedule="@hourly",
    start_date=pendulum.datetime(2023,6,25,tz="UTC"),
)as dag:

    read_json =PythonOperator(
               task_id='read_json',
               python_callable=read_fitness

    )

    save_cassandra =PythonOperator(
               task_id='save_cassandra',
               python_callable=save_fitness

    )

    read_json>>save_cassandra