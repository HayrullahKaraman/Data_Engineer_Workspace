
from datetime import datetime
import pandas as pd
from scripts.Extractdata import getdata

def transform():
   

    df_fuel = pd.json_normalize(data=getdata()['stations'],record_path='fuels',
                        meta=[['category','name']],errors='ignore')

    df_fuel.rename(columns={'name':'category_name'},inplace=True)
    df_fuel=df_fuel[['category','category_name','price','lastChange.amount','lastChange.timestamp']][0:300]

    df_v2=pd.json_normalize(getdata(),record_path=['stations'])
    df_station=df_v2[['country','id','name','brand','street','postalCode','place','isOpen','dist','volatility','coords.lat','coords.lng']][0:300]

    df=pd.concat([df_station,df_fuel],axis=1)

    df1=pd.DataFrame(df,columns=["country","id","name","brand","street","postalCode","place","isOpen","dist","volatility","coords.lat","coords.lng","category","category_name","price","lastChange.amount","lastChange.timestamp"])
    for _, row in df1.iterrows():
         to_json = row.to_dict() 
    return to_json