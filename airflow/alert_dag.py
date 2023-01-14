import pync
import os
import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
import time
from datetime import timedelta



dag = DAG(
    "alert_dag",
    schedule = timedelta(minutes=10),
    start_date=airflow.utils.dates.days_ago(2)
)


def alert_desktop_notification():
    folder = 'folderC'
    time_limit = 600  # 10 minutes in seconds

    for file in os.listdir(folder):
        if file.endswith('.csv'):
            file_path = os.path.join(folder, file)
            file_time = os.path.getmtime(file_path)
            if time.time() - file_time >= time_limit:
                pync.notify("New file in folderC")
                pync.notify(file)

            else:
                pync.notify("No new file in the last 10 minutes")



check_alert = PythonOperator(
    task_id="alert_dag",
    python_callable=alert_desktop_notification,
    dag=dag
)
