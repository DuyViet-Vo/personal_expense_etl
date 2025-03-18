from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from scripts.extract import extract_data
from scripts.transform import transform_data, generate_reports
from scripts.load import load_to_postgres, save_reports

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'expense_etl',
    default_args=default_args,
    description='ETL pipeline for personal expense analysis',
    schedule_interval='@daily',  # Chạy hàng ngày (có thể đổi thành @weekly, @monthly)
    start_date=datetime(2025, 3, 18),
    catchup=False,
) as dag:
    
    def extract_task():
        df = extract_data('data/expenses.csv')
        return df.to_json()  # Chuyển thành JSON để truyền qua XCom

    def transform_task(ti):
        df_json = ti.xcom_pull(task_ids='extract')
        df = pd.read_json(df_json)
        transformed_df = transform_data(df)
        weekly_report, monthly_report = generate_reports(transformed_df)
        return {
            'transformed': transformed_df.to_json(),
            'weekly': weekly_report.to_json(),
            'monthly': monthly_report.to_json()
        }

    def load_task(ti):
        data = ti.xcom_pull(task_ids='transform')
        transformed_df = pd.read_json(data['transformed'])
        weekly_report = pd.read_json(data['weekly'])
        monthly_report = pd.read_json(data['monthly'])
        
        load_to_postgres(transformed_df, 'expenses')
        save_reports(weekly_report, monthly_report)

    extract_op = PythonOperator(
        task_id='extract',
        python_callable=extract_task,
    )

    transform_op = PythonOperator(
        task_id='transform',
        python_callable=transform_task,
    )

    load_op = PythonOperator(
        task_id='load',
        python_callable=load_task,
    )

    extract_op >> transform_op >> load_op