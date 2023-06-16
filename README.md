AIRFLOW & DBT PROJECT FOR DATA & ANALYTICS ENGINEERS
========

Author: [Victor Iwuoha](https://linkedin/in/viciwuoha)


Project Contents
================
This Project is built using the astro cli provisioned by [Astronomer](https://docs.astronomer.io/)
To Run this project a linux environment is highly recommended.

Prerequisites:
- Linux Environment/ github codespaces/Ubuntu distribution on Windows
- Docker Compose
- A DBT Cloud Account (With an API Key)
- A .env file at the root of this directory with environment variables exactly as those in .env.example
- An accessible Postgres database with a valid connection URL.
- Basic Understanding of Python & SQL.


Steps for deployment

- Clone/Fork This Project to your github profile and connect it to your dbt account.
- Give DBT adequate access to connect to this repository on your git provider (github/gitlab) -> [see steps](https://docs.getdbt.com/docs/cloud/git/connect-github)
- Create a dbt project with the name airflow_dbt_magic and point it to the dbt subdirectory of this repository.
- Create a simple DBT JOB in the Production Environment called AIRFLOW DBT JOB and add the commands (dbt run, dbt docs generate). Note the Job Id as well as the account id as they would be needed in Airflow.

DBT:


- 1. Run the start.sh script
- 2. Trigger the Dag Named _**fakestore_elt_pipeline**_. If this Runs SuccessFully , The 


The Structure of this Project is explained on the aastonomer webpage.
===========================

Contact
=======

The Astronomer CLI is maintained with love by the Astronomer team. To report a bug or suggest a change, reach out to our support
