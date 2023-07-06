import requests
import pandas as pd
import json
from kafka import KafkaProducer
import time



def getdata():
    url='https://creativecommons.tankerkoenig.de/api/v4/stations/search?apikey=cffa4fb8-7a16-cd85-7946-263722530f15&lat=48.8&lng=9.24&rad=25'

    response = requests.get(url).json()
    df_fuel = pd.json_normalize(data=response['stations'],record_path='fuels',
                        meta=[['category','name']],errors='ignore')

    df_fuel.rename(columns={'name':'category_name'},inplace=True)
    df_fuel=df_fuel[['category','category_name','price','lastChange.amount','lastChange.timestamp']][0:300]

    df_v2=pd.json_normalize(response,record_path=['stations'])
    df_station=df_v2[['country','id','name','brand','street','postalCode','place','isOpen','dist','volatility','coords.lat','coords.lng']][0:300]

    df=pd.concat([df_station,df_fuel],axis=1)


    server="34.173.162.172:9092"
    topic_name='gas'
    producer = KafkaProducer(
        bootstrap_servers = server,
        value_serializer= lambda x: json.dumps(x).encode("utf-8"))

    for _, row in df.iterrows():
        to_json = row.to_dict()
        time.sleep(1)
        print(_)
        producer.send("gas", value=to_json)
        producer.flush()
        
    producer.close()

from airflow import DAG
from airflow.operators.python import PythonOperator
import pendulum
import os

with DAG(
    dag_id="1_gas_bash",
    schedule="@daily",
    start_date=pendulum.datetime(2023,6,11,tz="UTC")#Task Start date
    ) as dag:

    gas =  PythonOperator(
        task_id ="gas",#task name
        python_callable=getdata#Task execute
    )

    gas
