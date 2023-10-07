# when dataset is updated in db, this dag should trigger the dbt cloud run via the API
from datetime import datetime, timedelta

from airflow import DAG, Dataset
from airflow.models import Variable
from airflow.operators.empty import EmptyOperator
from airflow.providers.dbt.cloud.operators.dbt import DbtCloudRunJobOperator

from utils.utils import dag_owner, DBT_JOB_SCHEMA

# define arguments to be used in dag
dbt_job_id: int = Variable.get("datafest_meetup_job")
default_args = {
    "owner": dag_owner,
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="fakestore_dbt_job_pipeline",
    default_args=default_args,
    description="Simple Dag to Trigger Dbt Production Job",
    start_date=datetime(2023, 6, 11),
    schedule=[Dataset("//fakestore_dwh/tables")],
    catchup=False,
    tags=["airflow-dbt-magic"],
) as dag:
    start = EmptyOperator(task_id="start_pipeline")

    trigger_dbt_cloud_job = DbtCloudRunJobOperator(
        task_id="trigger_dbt_cloud_job",
        job_id=dbt_job_id,
        trigger_reason=f"Triggered From Airflow Dataset Update configured by {dag_owner}",
        steps_override=None,
        schema_override=DBT_JOB_SCHEMA,
        wait_for_termination=True,
        timeout=400,
        check_interval=60,
        additional_run_config=None,
    )

    start >> trigger_dbt_cloud_job
