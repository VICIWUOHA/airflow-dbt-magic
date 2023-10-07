import requests
import pandas as pd
import json
import os
from hashlib import md5
from datetime import datetime, timedelta
from pathlib import Path
from include.helper_scripts import transform_col_names

FAKE_STORE_ARTIFACTS = ["users", "products", "carts"]
pipeline_user = os.getenv("DATAFEST_23_USER")


class FakeStoreApiTransformer:
    """Transfromer Class for manipulating data from the FakeStoreApi at https://fakestoreapi.com/
    to deploy into a test datawarehouse. (This is not an exhaustive Class for all endpoints but PR's are welcome.)
    """

    def __init__(self) -> None:
        self.base_url = "https://fakestoreapi.com/"

    def get_fakestore_data(self, artifact: str, query_params: str = "") -> str:
        """Makes a call to https://fakestoreapi.com/ for a specified artifact/entity and simply writes to file storage

        Parameters
        ----------
        artifact : str
            The api endpoint/ db entity for which data should be gotten for.

        Returns
        -------
        str
            File Path where extracted Json data was written to.

        Raises
        ------
        Exception
            Any Exception encountered during REST API call or while writing to storage..
        """
        try:
            # make API call once and get json response
            with requests.Session() as s:
                print(f"=> Now Getting data for {artifact}")
                artifact_data = s.get(
                    self.base_url + f"{artifact}" + f"{query_params}"
                ).json()
            # write raw json to file storage:
            time_info = datetime.strftime(
                datetime.now() + timedelta(hours=1), "%Y_%m_%d_%H%M%S"
            )
            file_path = f"data_lake/{artifact}/"
            file_name = f"{artifact}_{time_info}.json"
            # check if file path exists and create if needed
            path_exists = os.path.exists(file_path)
            if not path_exists:
                f_path = Path(file_path)
                f_path.mkdir(parents=True)

            with open(file_path + file_name, "w", encoding="utf-8") as file:
                raw_data = json.dumps({f"{artifact}": artifact_data}, indent=4)
                file.write(raw_data)

            print(
                f"=> ``{artifact}`` data written successfully to ``{file_path+file_name}``."
            )
            return file_path + file_name

        except Exception as e:
            print("** Error while Calling API or writing to Data Lake.")
            raise e

    def transform_fakestore_data(
        self, artifact: str, json_file_path: str
    ) -> pd.DataFrame:
        """This Method Transforms defined artifacts from the FakeStoreApi as at 2023-06-15 , It supports
        (Users, Products & Carts) but can be extended.

        Parameters
        ----------
        artifact : str
            The defined artifact on of (Users, Products & Carts)
        json_file_path : str
            json file path on file storage which can be accessed from the airflow.
        Returns
        -------
        pd.DataFrame
            Normalized dataframe containing returned data from the Api in tabular format.
        """

        with open(json_file_path) as file:
            data = json.load(file)[artifact]
        print("=> Normalizing Dataset..")
        if artifact != "carts":
            artifact_data_trans = pd.json_normalize(data)
            artifact_data_trans["updated_at"] = datetime.strftime(
                datetime.now() + timedelta(hours=1), "%Y-%m-%d %H:%M:%S"
            )
            # artifact_data_trans
        else:
            artifact_data_trans = pd.json_normalize(
                data, record_path=["products"], meta=["id", "userId", "date"]
            )
            artifact_data_trans = artifact_data_trans.rename(columns={"id": "cart_id"})
            # create hash for item in cart purchased by user on a given date
            artifact_data_trans["id"] = (
                artifact_data_trans["date"]
                + artifact_data_trans["userId"].astype(str)
                + artifact_data_trans["productId"].astype(str)
            ).apply(lambda val: md5(val.encode()).hexdigest())
            artifact_data_trans = artifact_data_trans.reindex(
                columns=["cart_id", "id", "date", "userId", "productId", "quantity"]
            )

        # standardize column names
        artifact_data_trans.columns = transform_col_names(artifact_data_trans)
        # validate that users have added appropiate env vars during live demo and add their id's to all tables before writes
        print("=> Applying Identifiers..")
        assert (
            pipeline_user is not None
        ), "You must Include an env variable named DATAFEST_23_USER"
        artifact_data_trans["_datafest_meetup_user"] = pipeline_user
        artifact_data_trans["uuid"] = (
            artifact_data_trans["id"].astype(str)
            + artifact_data_trans["_datafest_meetup_user"]
        ).apply(lambda val: md5(val.encode()).hexdigest())
        artifact_data_clean = artifact_data_trans.drop(
            columns=["__v", "password"], errors="ignore"
        )
        return artifact_data_clean
