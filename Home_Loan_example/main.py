import codecs

import uvicorn
from typing import Dict
from fastapi import File
from fastapi import FastAPI
from database import SessionLocal, engine, conn_string
from fastapi import UploadFile
import numpy as np
import joblib
import pandas as pd
from pydantic import BaseModel
import psycopg2
from io import BytesIO
import json
import models



class Features(BaseModel):  # serializer

    Gender: int
    Married: int
    Education: int
    Self_Employed: int
    ApplicantIncome: int
    CoApplicantIncome: int
    LoanAmount: int
    Loan_Amount_Term: int
    Credit_History: int
    Property_Area : int


    class Config:
        orm_mode = True


db = SessionLocal()


app = FastAPI()

model = joblib.load('simple_logistic.joblib')


@app.get('/items', status_code=200)
def get_all_items():
    items = db.query(models.Features).all()

    return items


@app.post("/single-prediction")
async def predict(samples: Features):
    db_item = db.query(models.Features)
    # print(item)
    samples = samples.dict()

    Gender = str(samples['Gender'])
    Married = str(samples['Married'])
    Education = str(samples['Education'])
    Self_Employed = str(samples['Self_Employed'])
    ApplicantIncome = int(samples['ApplicantIncome'])
    CoApplicantIncome = float(samples['CoApplicantIncome'])
    LoanAmount = float(samples['LoanAmount'])
    Loan_Amount_Term= float(samples['Loan_Amount_Term'])
    Credit_History= float(samples['Credit_History'])
    Property_Area = str(samples['Property_Area'])

    #features = [1, 0, 1, 1, 12, 23.0, 12.0, 1.0, 1.0, 1]

    features = [int(Gender), int(Married), int(Education), int(Self_Employed), int(ApplicantIncome), int(CoApplicantIncome), int(LoanAmount), int(Loan_Amount_Term),
                int(Credit_History), int(Property_Area)]
    print(features)


    Loan_status = model.predict([features])
    print("Loan_status: ", Loan_status[0])
    new_status = int(Loan_status[0])
    features.append(new_status)
    print(features)

    db_user = models.Features(
    Gender = str(samples['Gender']),
    Married = str(samples['Married']),
    Education = str(samples['Education']),
    Self_Employed = str(samples['Self_Employed']),
    ApplicantIncome = int(samples['ApplicantIncome']),
    CoApplicantIncome = float(samples['CoApplicantIncome']),
    LoanAmount = float(samples['LoanAmount']),
    Loan_Amount_Term= float(samples['Loan_Amount_Term']),
    Credit_History= float(samples['Credit_History']),
    Property_Area = str(samples['Property_Area']),
    Loan_status = new_status)
    db.add(db_user)
    db.commit()


    return {'prediction': str(Loan_status[0])}


from fastapi.responses import HTMLResponse
from typing import Optional

@app.post("/multi-predictions")
async def create_upload_file(file: Dict):
    #print("got file")
    #db_item = db.query(models.Features)
    #test_csv = pd.read_csv(file.file)
    test_csv = pd.DataFrame.from_dict(file)

    #df2 = (test_csv.columns)
    #df instead of test_csv
    test_csv = test_csv.dropna().reset_index()
    test_csv.rename(columns={'CoapplicantIncome': 'CoApplicantIncome'}, inplace=True)
    test_csv = test_csv.drop(['Loan_ID', 'Dependents', 'index'], axis=1)
    test_csv.rename(columns={'index': 'Id'}, inplace=True)
    test_csv['Gender'] = test_csv['Gender'].replace('Male', '0').replace('Female', '1')
    test_csv['Married'] = test_csv['Married'].replace('Yes', '1').replace('No', '0')
    test_csv['Education'] = test_csv['Education'].replace('Graduate', '1').replace('Not Graduate', '0')
    test_csv['Self_Employed'] = test_csv['Self_Employed'].replace('Yes', '1').replace('No', '0')
    test_csv['Property_Area'] = test_csv['Property_Area'].replace('Urban', '1').replace('Rural', '0').replace(
        'Semiurban', '2')

    test_csv['Gender'] = pd.to_numeric(test_csv['Gender'])
    test_csv['Married'] = pd.to_numeric(test_csv['Married'])
    test_csv['Education'] = pd.to_numeric(test_csv['Education'])
    test_csv['Self_Employed'] = pd.to_numeric(test_csv['Self_Employed'])
    test_csv['Property_Area'] = pd.to_numeric(test_csv['Property_Area'])
    test_csv['CoApplicantIncome'] = test_csv['CoApplicantIncome'].astype(float)

    model = joblib.load('simple_logistic.joblib')
    Loan_status = model.predict(test_csv)
    # print(Loan_status[0])
    for i in range(len(test_csv)):
        test_csv['Loan_status'] = Loan_status[i]
        print(test_csv.head())
        print(test_csv.columns)

        print("Loan status", Loan_status[i])

        conn = engine.connect()

        test_csv = test_csv.drop_duplicates(keep='first')

        test_csv.to_sql('home_loan_predictions17', con=conn, if_exists='replace')

        conn = psycopg2.connect(conn_string)

        #conn.autocommit = True
        cursor = conn.cursor()

        conn.commit()
        # conn.close()
        print("sent to db.")

    #file.file.close()
    #test_csv_json = test_csv.to_dict('split')
    print(test_csv)
    #return {"filename": str(file.filename)}
    print("returned")
    return {"message": "success"}



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
