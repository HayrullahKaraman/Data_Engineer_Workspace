
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import pendulum
from datetime import timedelta
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryExecuteQueryOperator
from scripts.Transformdata import transform
from scripts.Extractdata import getdata
from scripts.LoadDatagGCP import load

PROJECT_NAME = "stoked-cosine-391507"
DB_NAME = "gas"

with DAG(
    dag_id="GCP_ETL",
    schedule="@daily",
    start_date=pendulum.datetime(2023,6,25,tz="UTC"),
)as dag:
    

    extract_data=PythonOperator(
            task_id="extract_data",
            python_callable= getdata
      )
    transform_data=PythonOperator(
            task_id="transform_data",
            python_callable=transform
      )
    
    load_data=PythonOperator(
            task_id="load_data",
            python_callable= load
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
    
    query_gasoline=f"SELECT * FROM {PROJECT_NAME}.{DB_NAME}.gas_table where category = 'gasoline'"
    query_diesel=f"SELECT * FROM {PROJECT_NAME}.{DB_NAME}.gas_table where category = 'diesel'"

    create_gasoline_table = BigQueryExecuteQueryOperator(
        task_id='create_gasoline_table',
        sql=query_gasoline,
        destination_dataset_table=f"{PROJECT_NAME}.{DB_NAME}.gasoline_table",
        create_disposition="CREATE_IF_NEEDED",#If Table dont create 
        write_disposition="WRITE_TRUNCATE",
        use_legacy_sql=False,
        gcp_conn_id="Google_Cloud_Con"
    )
    
    create_diesel_table = BigQueryExecuteQueryOperator(
        task_id='create_diesel_table',
        sql=query_diesel,
        destination_dataset_table=f"{PROJECT_NAME}.{DB_NAME}.diesel_table",
        create_disposition="CREATE_IF_NEEDED",#If Table dont create 
        write_disposition="WRITE_TRUNCATE",
        use_legacy_sql=False,
        gcp_conn_id="Google_Cloud_Con"
    )



    extract_data >> [transform_data , load_data ] >> load_data_from_gsc >> [create_gasoline_table,create_diesel_table]