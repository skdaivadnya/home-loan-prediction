
import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
import great_expectations as ge
from datetime import timedelta
from datetime import datetime
from great_expectations.exceptions import GreatExpectationsValidationError

# Define the DAG
dag = DAG(
    "check_csv_dag",
    schedule = timedelta(minutes=15),
    start_date=airflow.utils.dates.days_ago(2)
)

# Define the task
def check_csv_task():
    # Load the data
    data = pd.read_csv("/Users/suryatejasista/Documents/airflow/folderA/test (2).csv")

    sample = data.sample(1)

    print(pd.DataFrame(sample))
    df_ge = ge.dataset.PandasDataset(sample)
    # Checking whether the sample meets the constraint
    try:
        result1 = df_ge.expect_column_values_to_not_be_null("Dependents")
        print("result1:", result1)
        result2 = df_ge.expect_column_values_to_be_unique('Loan_ID')
        print("result2:", result2)
        result3 = df_ge.expect_column_values_to_not_be_null("Gender")
        print("result3:", result3)
        result4 = df_ge.expect_column_values_to_not_be_null("Credit_History")
        print("result4:", result4)
        result5 = df_ge.expect_column_values_to_be_of_type(column="Credit_History", type_="int")
        print("result5:", result5)

        if result1['success'] and result2['success'] and result3['success'] and result4['success'] or result5['success']:
           sample.to_csv(f'/Users/suryatejasista/Documents/airflow/folderB/{datetime.now().strftime("%Y-%M-%d_%H-%M-%S")}.csv',
                                index=False)

           print("folderB notification sent")

        else:
            print("data quality failed")
            sample.to_csv(
                f'/Users/suryatejasista/Documents/airflow/folderC/{datetime.now().strftime("%Y-%M-%d_%H-%M-%S")}.csv',
                index=False)

    except ge.exceptions.GreatExpectationsValidationError as e:

        print("entered into except")


check_csv_operator = PythonOperator(
    task_id="check_csv_task",
    python_callable=check_csv_task,
    dag=dag
)
