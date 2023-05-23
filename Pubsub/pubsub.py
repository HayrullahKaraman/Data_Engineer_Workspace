import json
from google.cloud import pubsub_v1
from concurrent import futures
from typing import Callable
import os


import jsonlines
import json

from google.cloud import pubsub_v1#pip install google-cloud-pubsub
import os 
import json
from bs4 import BeautifulSoup as bts
import requests
import pandas as pd
import numpy as np


def getAndParseURL(url):
    result = requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'})
    soup = bts(result.text, 'html.parser')
    return soup

PAGE = []
for page_list in range(1,51):
    PAGE.append('https://coinmarketcap.com/?page='+ str(page_list))

TITLE= []
PRICE= []
HOUR1=[]
VOLUME24=[]
MARKETCAP=[]
for product in PAGE[::]:
    soup =getAndParseURL(product)
   
    for title_all_page in soup.find_all("p",{"class":"sc-4984dd93-0 iqdbQL coin-item-symbol"}):
        try:
            TITLE.append(title_all_page.text)
        except:
            TITLE.append(np.nan)
            
    for price_all_page in soup.find_all("div",{"class":"sc-cadad039-0 clgqXO"}):
        try:
            PRICE.append(price_all_page.text.replace('$',''))
        except:
            PRICE.append(np.nan)
            
    for hour1_all_page in soup.find_all("span",{"class":"sc-97d6d2ca-0 cYiHal"}):
        try:
            HOUR1.append(hour1_all_page.text.replace('%','').replace('\n',''))
        except:
            HOUR1.append(np.nan)
    
    for volume24_all_page in soup.find_all("div",{"class":"sc-aef7b723-0 sc-8085623a-0 jIjTQr"}):
        try:
            VOLUME24.append(volume24_all_page.text.strip().replace('$',''))
        except:
            VOLUME24.append(np.nan)
                            
    for marketcap_all_page in soup.find_all("span",{"class":"sc-edc9a476-0 fXzXSk"}):
        try:
            MARKETCAP.append(marketcap_all_page.text.strip().replace('$',''))
        except:
            MARKETCAP.append(np.nan)

print("prepring dataframe")

df=pd.DataFrame(list(zip(TITLE,PRICE,HOUR1,VOLUME24,MARKETCAP)),columns=['title','price','hour1','volume24','marketcap'])
#df.marketcap= df.marketcap.map(lambda x: str(x)[:-1])
#df.marketcap= pd.to_numeric(df.marketcap , errors='coerce')
df.replace('(^\s+|\s+$)', '', regex=True, inplace=True)
df.to_json('Coinmarketcap1.json',orient="records",lines=True)
print("prepring json")


def publish_message(project_id, topic_name, message):
    # Pub/Sub istemcisini oluştur
    publisher = pubsub_v1.PublisherClient()
    
    # Mesaj verisini JSON formatına dönüştür
    message_data = json.dumps(message).encode('utf-8')
    
    # Mesajı Pub/Sub'a gönder
    topic_path = publisher.topic_path(project_id, topic_name)
    future = publisher.publish(topic_path, data=message_data)
    future.result()
    
    print('Mesaj Pub/Sub\'a başarıyla gönderildi.')

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'nth-autumn-381608-1ce92bbf6075.json'
# Pub/Sub proje ID'si
project_id = 'nth-autumn-381608'

# Mesaj gönderilecek topic adı
topic_name = 'coinv7'



for _, row in df.iterrows():
    to_json = row.to_dict()
    message=to_json
    publish_message(project_id, topic_name, message)