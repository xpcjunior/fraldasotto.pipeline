from io import StringIO
import requests
import pandas as pd
from pandas import DataFrame


class GSheetTab():

    def __init__(self, id: str) -> None:
        self.__sheet_url = f'https://docs.google.com/spreadsheets/d/{id}/export?format=csv'

    def download_tab(self, tab_id: str) -> DataFrame:
        url = f'{self.__sheet_url}&gid={tab_id}'
        return pd.read_csv(url)
