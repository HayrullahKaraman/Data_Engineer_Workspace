from fastapi import FastAPI
import pickle 
import pandas as pd
from pydantic import BaseModel
from joblib import load

app= FastAPI()

class modelShema(BaseModel):
    text:str



app.get("/")
def hello():
     return{"mesaj":"Welcome"}

@app.post("/predict")
def predict_model(predictvalue:modelShema):
    model = load("smap_mail_lr.pkl")
    df= pd.DataFrame(
        [predictvalue.dict().values()],
        columns=predictvalue.dict().keys()
    )

    pred=model.predict(df)
    return{"Predict":int(pred[0])}