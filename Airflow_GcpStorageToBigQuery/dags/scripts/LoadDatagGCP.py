from datetime import datetime
import os
from google.cloud import storage
import pandas as pd
import sys
#from pathlib import Path
#sys.path.append(str(Path('/opt/airflow/dags/scripts/Transformdata.py').resolve()))
from scripts.Transformdata import transform


def load():
    df=pd.DataFrame.from_dict([transform()])

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/opt/airflow/dags/scripts/stoked-cosine-391507-fc18e1ccc108.json'

    settime = datetime.now()#for filename 
    filetime = settime.strftime("%Y")+ "_"+settime.strftime("%m") +"_"+settime.strftime("%d") +"_"+settime.strftime("%H") +"_"+settime.strftime("%M")  +"_"+settime.strftime("%S") 
    file_name=f'gas-{filetime}.csv'
                
    client= storage.Client()
    bucket=client.bucket("tanker_data")
    bucket.blob(file_name).upload_from_string(df.to_csv(index=False, encoding='utf-8'),content_type='application/octet-stream')