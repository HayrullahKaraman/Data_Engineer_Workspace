from google.cloud import pubsub_v1
import requests
import json
import pandas as pd
import os

url='https://financialmodelingprep.com/api/v3/historical-price-full/AAPL?apikey=d8ff7cb62ac0e084cb1cc9c5aa27357a'

response = requests.get(url).json()
df = pd.json_normalize(response, record_path=['historical'])

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'nth-autumn-381608-2b71f7276aa6.json'
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


# Pub/Sub proje ID'si
project_id = 'nth-autumn-381608'

# Mesaj gönderilecek topic adı
topic_name = 'finance'



for _, row in df.iterrows():
    to_json = row.to_dict()
    message=to_json
    publish_message(project_id, topic_name, message)