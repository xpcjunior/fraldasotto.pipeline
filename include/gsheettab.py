from io import StringIO
from airflow.providers.http.hooks.http import HttpHook
import pandas as pd
from pandas import DataFrame


class GSheetTab():

    def __init__(self) -> None:
        self.http_hook = HttpHook(
            method="GET",
            http_conn_id="fraldas_otto_gsheet"
        )

    def download_tab(self, tab_id: str) -> DataFrame:
        response = self.http_hook.run(
            '/export', # Endpoint
            data={
                'format': 'csv',
                'gid': tab_id
            }
        )
        
        if response.status_code == 200:
            return pd.read_csv(StringIO(response.text))
        else:
            raise Exception(f"Erro ao baixar a planilha: {response.status_code}, {response.text}")
