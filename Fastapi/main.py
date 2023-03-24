#read db
import psycopg2 
def connnection_db():
       conn=psycopg2.connect(
               database="weather",
                user="masal",
                password="Masal2020",
                host="localhost",
                port="5432"  
                )
       return conn




# #Fast api
from fastapi  import FastAPI,Depends

# # """
# # get=select
# # post=insert
# # pull=update
# # delete=delete
# #  """
app = FastAPI()

# @app.get("/")
# def hello():
#      return{"mesaj"}

@app.get("/")
def get_weather(conn = Depends(connnection_db)):
    try:
           cursor=conn.cursor()
           cursor.execute("SELECT * FROM weathertable")
           rows=cursor.fetchall()
           conn.close()
    except:
           return{"Connecion was error"}
    return rows        

