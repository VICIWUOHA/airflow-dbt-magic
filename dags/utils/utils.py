import os

dag_owner = os.getenv("DBT_LAGOS_MEETUP_USER")
DBT_JOB_SCHEMA = "dbt_" + dag_owner
