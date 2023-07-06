from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import pendulum
import json
import datetime
import requests
import os
from google.cloud import storage
import pandas as pd
from datetime import timedelta
from datetime import datetime

from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryExecuteQueryOperator

def getdata():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/opt/airflow/dags/scripts/stoked-cosine-391507-fc18e1ccc108.json'
    url='https://creativecommons.tankerkoenig.de/api/v4/stations/search?apikey=cffa4fb8-7a16-cd85-7946-263722530f15&lat=48.8&lng=9.24&rad=25'

    response = requests.get(url).json()
    df_fuel = pd.json_normalize(data=response['stations'],record_path='fuels',
                        meta=[['category','name']],errors='ignore')

    df_fuel.rename(columns={'name':'category_name'},inplace=True)
    df_fuel=df_fuel[['category','category_name','price','lastChange.amount','lastChange.timestamp']][0:300]

    df_v2=pd.json_normalize(response,record_path=['stations'])
    df_station=df_v2[['country','id','name','brand','street','postalCode','place','isOpen','dist','volatility','coords.lat','coords.lng']][0:300]

    df=pd.concat([df_station,df_fuel],axis=1)

    df1=pd.DataFrame(df,columns=["country","id","name","brand","street","postalCode","place","isOpen","dist","volatility","coords.lat","coords.lng","category","category_name","price","lastChange.amount","lastChange.timestamp"])

    
    

    settime = datetime.now()#for filename 
    filetime = settime.strftime("%Y")+ "_"+settime.strftime("%m") +"_"+settime.strftime("%d") +"_"+settime.strftime("%H") +"_"+settime.strftime("%M")  +"_"+settime.strftime("%S") 

    file_name=f'gas-{filetime}.csv'
    
    client= storage.Client()
    bucket=client.bucket("tanker_data")
    
    
    bucket.blob(file_name).upload_from_string(df1.to_csv(index=False, encoding='utf-8'),content_type='application/octet-stream')

PROJECT_NAME = "stoked-cosine-391507"
DB_NAME = "gas"

with DAG(
    dag_id="EtL_Python",
    schedule="@hourly",
    start_date=pendulum.datetime(2023,6,25,tz="UTC"),
)as dag:
    

    extract_data_from_metro=PythonOperator(
            task_id="extract_data_from_metro",
            retries= 2,
            retry_delay= timedelta(minutes=10),
            python_callable=getdata
      )
    
  

    load_data_from_gsc=GCSToBigQueryOperator(
        task_id="load_data_from_gsc",
        bucket="tanker_data",#Bucket Name
        source_objects=["*.csv"],
        source_format="CSV",#Format
        skip_leading_rows=1,#first_column
        field_delimiter=",",
        destination_project_dataset_table=f"{PROJECT_NAME}.{DB_NAME}.gas_table",#Table Name
        create_disposition="CREATE_IF_NEEDED",#If Table dont create 
        write_disposition="WRITE_TRUNCATE",
        #WRITE_EMPTY
        #WRITE_APPEND
        #WRITE_TRUNCATE
        gcp_conn_id="Google_Cloud_Con"#Connection On Airflow
    )
    
    extract_data_from_metro >> load_data_from_gsc
    