from datetime import timedelta
import pandas as pd
from pandas import DataFrame
import pendulum


class Transform():

    def __init__(
            self, data_execucao_dag: str,
            df_ganhadas: DataFrame, df_compradas: DataFrame, df_utilizadas: DataFrame
    ) -> None:
        self.__data_execucao_dag = pendulum.parse(data_execucao_dag)
        self.__df_ganhadas = df_ganhadas
        self.__df_compradas = df_compradas
        self.__df_utilizadas = df_utilizadas

    def __getQTD(self, df: DataFrame, tamanho: str, nome_qtd: str) -> str:
        try:
            return str(df.loc[df['tamanho'] == tamanho, nome_qtd].iloc[0])
        except:
            return '0'

    def get_transformed_data(self):

        df_estoque = pd.concat(
            [self.__df_compradas, self.__df_ganhadas],
            ignore_index=True
        ).drop(columns=['valor', 'evento'])

        df_estoque_gp = pd.DataFrame(df_estoque.groupby(['tamanho'])['quantidade'].sum()).reset_index()
        df_utilizadas_gp = pd.DataFrame(self.__df_utilizadas.groupby(['tamanho'])['quantidade'].sum()).reset_index()

        df_estoque_gp = df_estoque_gp.merge(df_utilizadas_gp, on='tamanho', how='left', suffixes=('', '_utilizadas'))
        df_estoque_gp['quantidade_utilizadas'] = df_estoque_gp['quantidade_utilizadas'].fillna(0)
        df_estoque_gp['quantidade_utilizadas'] = df_estoque_gp['quantidade_utilizadas'].astype('int64')

        df_estoque_gp['qtd_restante'] = df_estoque_gp['quantidade'] - df_estoque_gp['quantidade_utilizadas']
        
        data_hora_fuso = self.__data_execucao_dag + timedelta(hours=-3)
        
        return {
            "data": data_hora_fuso.strftime("%d/%m/%Y %H:%M"),
            "relatorio": [
                {
                    "tamanho": "RN",
                    "fraldas": {
                        "estoque": self.__getQTD(df_estoque_gp, 'RN', 'quantidade'),
                        "utilizadas": self.__getQTD(df_estoque_gp, 'RN', 'quantidade_utilizadas'),
                        "restantes": self.__getQTD(df_estoque_gp, 'RN', 'qtd_restante')
                    }
                },
                {
                    "tamanho": "RN+",
                    "fraldas": {
                        "estoque": self.__getQTD(df_estoque_gp, 'RN+', 'quantidade'),
                        "utilizadas": self.__getQTD(df_estoque_gp, 'RN+', 'quantidade_utilizadas'),
                        "restantes": self.__getQTD(df_estoque_gp, 'RN+', 'qtd_restante')
                    }
                },
                {
                    "tamanho": "P",
                    "fraldas": {
                        "estoque": self.__getQTD(df_estoque_gp, 'P', 'quantidade'),
                        "utilizadas": self.__getQTD(df_estoque_gp, 'P', 'quantidade_utilizadas'),
                        "restantes": self.__getQTD(df_estoque_gp, 'P', 'qtd_restante')
                    }
                },
                {
                    "tamanho": "M",
                    "fraldas": {
                        "estoque": self.__getQTD(df_estoque_gp, 'M', 'quantidade'),
                        "utilizadas": self.__getQTD(df_estoque_gp, 'M', 'quantidade_utilizadas'),
                        "restantes": self.__getQTD(df_estoque_gp, 'M', 'qtd_restante')
                    }
                },
                {
                    "tamanho": "G",
                    "fraldas": {
                        "estoque": self.__getQTD(df_estoque_gp, 'G', 'quantidade'),
                        "utilizadas": self.__getQTD(df_estoque_gp, 'G', 'quantidade_utilizadas'),
                        "restantes": self.__getQTD(df_estoque_gp, 'G', 'qtd_restante')
                    }
                }
            ]
        }