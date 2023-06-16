AIRFLOW & DBT PROJECT FOR DATA & ANALYTICS ENGINEERS
========

*Author: [Victor Iwuoha](https://linkedin/in/viciwuoha)*

*Date: 16th June 2023*

*Event: DBT-Lagos-Meetup*

&nbsp;
Project Contents
================
This Project is built using the astro cli provisioned by [Astronomer](https://docs.astronomer.io/)
To Run this project a linux environment is highly recommended.


#### Prerequisites:

- Linux Environment/ github codespaces/Ubuntu distribution on Windows
- Docker Compose
- A DBT Cloud Account (With an API Key)
- A .env file at the root of this directory with environment variables exactly as those in .env.example but with actual values.
- An accessible Postgres database with a valid connection URL.
- Basic Understanding of Python & SQL.


#### Steps for deployment:

- Clone/Fork This Project to your github profile and connect it to your dbt account.
- Give DBT adequate access to connect to this repository on your git provider (github/gitlab) -> [see steps](https://docs.getdbt.com/docs/cloud/git/connect-github)
- Create a dbt project with the name airflow_dbt_magic and point it to the dbt subdirectory of this repository.
- Create a simple DBT JOB in the Production Environment called AIRFLOW DBT JOB and add the commands (dbt build, dbt snapshot dbt docs generate). Note the **Job Id** as well as the **Account id** as they would be needed in Airflow.


#### Execution:

- 1. Run the start.sh script. This should start your project, export all environment variables and create a **data_lake/** dir.
- 2. Turn on the two **fakestore_** dags and Trigger the Dag Named _**fakestore_elt_pipeline**_. If this Runs SuccessFully , the _**fakestore_dbt_dag**_ would automagically get triggered based on the dataset schedule. See more on [Airflow Datasets](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/datasets.html)
- 3. Wait for the dbt dag to complete running and navigate to the dbt cloud UI to see that the dag was triggered via the API. For more notes on the operation of this dag, see [DbtCloudOperator](https://airflow.apache.org/docs/apache-airflow-providers-dbt-cloud/stable/operators.html). In Standard practices, there are packages that can be used with dbt core to convert your entire dbt project into airflow tasks for easier management. An example is [Astronomer Cosmos](https://github.com/astronomer/astronomer-cosmos)

Credits:
===========================

The Structure of this project was adapted from the astronomer provided astro cli and created using astro dev init
Docs are available at the following Links

- [Apache Airflow]()
- [Astronomer](https://docs.astronomer.io/)
- [DBT Cloud](https://docs.getdbt.com/) and [DBT-Cloud-Airflow Example](https://docs.getdbt.com/guides/orchestration/airflow-and-dbt-cloud/1-airflow-and-dbt-cloud)

The compilation of this project was inspired with :love by the **dbt-lagos-community** :celebration .


===========================