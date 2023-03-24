import requests

def weather():
    url_link = "http://api.weatherapi.com/v1/current.json"
    access_key="d52ce3623d714a968ef181801231003"


    citys = ["Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Aksaray", "Amasya", "Ankara",
             "Antalya", "Ardahan", "Artvin", "Aydın", "Balıkesir", "Bartın", "Batman", "Bayburt", "Bilecik", "Bingöl", 
             "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Düzce", "Edirne", 
             "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkâri", "Hatay", "Iğdır", "Isparta",
             "İstanbul", "İzmir", "Kahramanmaraş", "Karabük", "Karaman", "Kars", "Kastamonu", "Kayseri", "Kilis", "Kırıkkale", "Kırklareli", 
             "Kırşehir", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Mardin", "Mersin", "Muğla", "Muş", "Nevşehir", "Niğde", "Ordu",
             "Osmaniye", "Rize", "Sakarya", "Samsun", "Şanlıurfa", "Siirt", "Sinop", "Sivas", "Şırnak", "Tekirdağ", "Tokat", "Trabzon", "Tunceli", 
             "Uşak", "Van", "Yalova", "Yozgat", "Zonguldak"]

    
    data = []
    
    for city in citys:
        re= requests.get(url=url_link,params={"key":access_key,"q":f"{city}"}).json()
        try:
            if re["current"]["temp_c"] < 10:
                values={
                        "City":re["location"]["name"],
                        "Temp":re["current"]["temp_c"],
                        "Date":re["location"]["localtime"],
                        "Text":re["current"]["condition"]["text"]
                }
                data.append(values)
            else:
                continue
        except:
              continue
    return data



#Write DB
import psycopg2 

conn=psycopg2.connect(
                database="weather",
                user="masal",
                password="Masal2020",
                host="localhost",
                port="5432"  
                )




conn.cursor().execute('''CREATE TABLE IF NOT EXISTS weathertable
               (id SERIAL  PRIMARY KEY,
               City TEXT,
               Temp Real,
               Date date,
               Text TEXT)''')      
conn.commit()



weather_db=weather()
sql="""INSERT INTO weathertable (City,Temp,Date,Text) VALUES (%s,%s,%s,%s);"""

# #write to disct
for data in weather_db:
     conn.cursor().execute(sql,(data["City"],data["Temp"],data["Date"],data["Text"]))

conn.commit()
conn.close()


