import pandas as pd
import re
import os
from typing import List, Literal
from time import sleep
from sqlalchemy import create_engine


def transform_col_names(dataset: pd.DataFrame) -> List[str]:
    """Transformer function to change CamelCases to sql friendly snake_case and handle irregularities in field names.
    Parameters
    ----------
    dataset : pd.DataFrame
        DataFrame for which a column name transformation is needed

    Returns
    -------
    List[str]
        List of transformed column names to be mapped to the original dataframe.
    """

    old_col_list = dataset.columns.to_list()
    new_col_list = []
    for col in old_col_list:
        # change from CamelCase to snake_case
        col_name = re.sub("([a-z])([A-Z0-9])", r"\1_\2", col)
        # replace dots with underscores
        new_name = col_name.replace("name.", "").replace(".", "_")
        new_col_list.append(new_name.lower())

    return new_col_list


def load_to_db(
    table_name: str,
    dataset: pd.DataFrame,
    db_name: str = os.getenv("DBT_LAGOS_MEETUP_DB"),
    schema: str = "dbt_" + str(os.getenv("DBT_LAGOS_MEETUP_USER")),
    if_exists="append",
) -> Literal[True]:
    """Connects to a Database and Loads a supplied Dataframe to a specific schema and table in that Database

    Parameters
    ----------
    db_name : str
        The database to connect to
    table_name : str
        The table to be loaded with data
    dataset : pd.DataFrame
       data to be loaded to db table
    schema : str, optional
        schema of the database to be operated upon ->default: dev
    if_exists : str, optional
        Logic to apply if the table already exists -> default: appends to table. "append"

    Returns
    -------
    boolean|None
        True if load action was successful otherwise Nothing is returned.

    Raises
    ------
    Exception
       Any SqlAlchemy Engine Connection Error encountered.
    Exception
        Any Exception after connection that occurs during database load operation.
    """
    print("=> Connecting to Database......")
    try:
        DEV_ENV = os.getenv("ENV_PG_DB_URI")
        engine = create_engine(f"{DEV_ENV}/{db_name}")
        conx = engine.connect()
        message = "=>Successfully Established Connection to Database"
        print(message)
    except Exception as e:
        error_log = "Pipeline Broken,Connection to Database Failed : {}".format(e)
        print(error_log)
        raise e
    print("=> Writing Data to Database.....")
    sleep(2)
    try:
        dataset.to_sql(
            f"{table_name}", con=conx, schema=schema, if_exists=if_exists, index=False
        )
        message = (
            "***==> Successfully Written `{}` Rows of Data to db: `{}.{}.{}` .".format(
                len(dataset), db_name, schema, table_name
            )
        )
        conx.close()
        print(message)
        return True
    except Exception as e:
        error_log = "Pipeline Broken,Failed to Write data to Database : {}".format(e)
        print(error_log)
        raise e
