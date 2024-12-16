from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import os
import subprocess


# Arguments 
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


# DAG 
with DAG(
    'web_harvesting_pipeline',
     default_args=default_args,
    description='Web scraping pipeline for property data',
     schedule_interval=None,  
    start_date=datetime(2023, 12, 1),
     catchup=False,
) as dag:

# Ddirectory for scripts
    scripts_dir = os.path.join('/app', 'web_harvesting')

# Task: Step 1 - Scrape property list
    def run_step1():
        subprocess.run(['python',os.path.join(scripts_dir, 'step1_scrape_list.py')], check=True)

    step1_task = PythonOperator(
         task_id='scrape_property_list',
        python_callable=run_step1,
    )
# Task: Step 2 - Scrape property details
    def run_step2():
        subprocess.run(['python', os.path.join(scripts_dir, 'step2_scrape_details.py')], check=True)

    step2_task = PythonOperator(
         task_id='scrape_property_details',
        python_callable=run_step2,
    )
# Task: Step 3 - Scrape property images
    def run_step3():
        subprocess.run(['python', os.path.join(scripts_dir, 'step3_scrape_images.py')], check=True)

    step3_task = PythonOperator(
        task_id='scrape_property_images',
         python_callable=run_step3,
    )  
#  task dependencies
    step1_task >> step2_task >> step3_task
