from datetime import datetime, timedelta
from airflow import Dataset
from airflow.decorators import (
    dag,
    task,
)

# import astro.sql as aql
# from astro.sql.table import Table
from airflow.operators.empty import EmptyOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from include.transformers import FakeStoreApiTransformer, FAKE_STORE_ARTIFACTS
from include.helper_scripts import load_to_db
from utils.utils import dag_owner, DBT_JOB_SCHEMA

dag_docs = """ This DAG gets and transforms fictitious retail data from http://fakestoreapi.com into a data warehouse.
                It also implements airflow concepts such as;

    - `task.expand()`  for dynamic mapping
    - airflow `Datasets` for Data aware scheduling used to trigger a DBT DAG run in fakestore_dbt_dag

            """


@dag(
    dag_id="fakestore_elt_pipeline",
    start_date=datetime(2023, 6, 11),
    # This defines how many instantiations of this DAG (DAG Runs) can execute concurrently. In this case,
    # we're only allowing 1 DAG run at any given time, as opposed to allowing multiple overlapping DAG runs.
    max_active_runs=1,
    schedule_interval="@daily",
    # Default settings applied to all tasks within the DAG; can be overwritten at the task level.
    default_args={
        "owner": f"{dag_owner}",  # This defines the value of the "owner" column in the DAG view of the Airflow UI
        "retries": 1,  # If a task fails, it will retry 2 times.
        "retry_delay": timedelta(
            seconds=30
        ),  # A task that fails will wait 30 seconds to retry.
    },
    catchup=False,
    tags=["airflow-dbt-magic"],
    doc_md=dag_docs,
)
def data_elt_process():
    create_destination_schema_and_tables = PostgresOperator(
        task_id="create_destination_tables_if_not_exists",
        postgres_conn_id="postgres_default",
        sql="utils/ddl_scripts.sql",
        params={"schema": DBT_JOB_SCHEMA},
    )

    transformer = FakeStoreApiTransformer()

    @task(max_active_tis_per_dag=1)
    def get_and_load_data(artifact: str, ti=None):
        file_path = transformer.get_fakestore_data(artifact)
        ti.xcom_push(key="uploaded_file_paths", value=file_path)

    upload_files = get_and_load_data.expand(artifact=FAKE_STORE_ARTIFACTS)

    transform_tasks = []
    # run transform tasks in parallel
    for artifact in FAKE_STORE_ARTIFACTS:

        @task(task_id=f"transform_and_load_{artifact}")
        def transform_and_load(artifact: str, ti=None):
            print("=> Transforming data.........")

            file_paths = list(ti.xcom_pull(key="uploaded_file_paths"))
            file_to_transform = [file for file in list(file_paths) if artifact in file][
                0
            ]
            transformed_data = transformer.transform_fakestore_data(
                artifact=f"{artifact}", json_file_path=file_to_transform
            )
            # load to db
            load = load_to_db(table_name=artifact, dataset=transformed_data)
            if load:
                return load

        transform_and_load_task = transform_and_load(artifact=artifact)
        transform_tasks.append(transform_and_load_task)

    end_pipeline = EmptyOperator(
        task_id="end_pipeline",
        trigger_rule="none_failed",
        outlets=[Dataset("//fakestore_dwh/tables")],
    )

    # enforce dependencies
    (
        create_destination_schema_and_tables
        >> upload_files
        >> transform_tasks
        >> end_pipeline
    )


dag_run = data_elt_process()
