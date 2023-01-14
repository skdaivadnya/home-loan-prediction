
import time
from datetime import timedelta
import pandas as pd
import requests
import json
import os
import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
os.environ["no_proxy"]="*"


dag = DAG(
    "predict_seven_data",
    schedule = timedelta(minutes=5),
    start_date=airflow.utils.dates.days_ago(2)
)

def predict_good_seven_data():
    folder = 'folderC'
    time_limit = 600  # 10 minutes in seconds

    for file in os.listdir(folder):
        if file.endswith('.csv'):
            file_path = os.path.join(folder, file)
            file_time = os.path.getmtime(file_path)
            if time.time() - file_time <= time_limit:
                file_list = os.listdir(folder)
                file_list
                df_append = pd.DataFrame()
                for file in file_list:
                    df_temp = pd.read_csv(folder + '/' + file)
                    df_append = df_append.append(df_temp, ignore_index=True)
                df = df_append
                #df2 = df.to_csv("/Users/suryatejasista/Documents/airflow/folderD/newdata.csv")
                response = requests.post('http://127.0.0.1:8000/multi-predictions', data=json.dumps(df.to_dict()))
                print(response.json())
                print(f'{file} was inserted within the last 10 minutes.')
            else:
                print(f'{file} was not inserted within the last 10 minutes.')



check_csv_prediction_seven = PythonOperator(
    task_id="check_csv_prediction_seven",
    python_callable=predict_good_seven_data,
    dag=dag
)
