import os

dag_owner = os.getenv("DATAFEST_23_USER")
DBT_JOB_SCHEMA = "dbt_" + dag_owner
