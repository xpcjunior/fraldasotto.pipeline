from airflow import DAG
from airflow.models import TaskInstance, Variable
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

from include.gsheettab import GSheetTab
from include.transform import Transform
from include.load import Load


load = Load()
gsheet = GSheetTab()

def extracao(ti: TaskInstance = None):
    df_ganhadas = gsheet.download_tab(Variable.get("ID_TAB_G_SHEET_GANHADAS"))
    df_compradas = gsheet.download_tab(Variable.get("ID_TAB_G_SHEET_COMPRADAS"))
    df_utilizadas = gsheet.download_tab(Variable.get("ID_TAB_G_SHEET_UTILIZADAS"))

    ti.xcom_push(key=f'dataframe_ganhadas', value=df_ganhadas)
    ti.xcom_push(key=f'dataframe_compradas', value=df_compradas)
    ti.xcom_push(key=f'dataframe_utilizadas', value=df_utilizadas)

def transformacao(ti: TaskInstance = None, data_execucao: str = None):
    df_ganhadas = ti.xcom_pull(key=f'dataframe_ganhadas', task_ids='extracao_tabs_g_sheets')
    df_compradas = ti.xcom_pull(key=f'dataframe_compradas', task_ids='extracao_tabs_g_sheets')
    df_utilizadas = ti.xcom_pull(key=f'dataframe_utilizadas', task_ids='extracao_tabs_g_sheets')

    transf = Transform(data_execucao, df_ganhadas, df_compradas, df_utilizadas)
    json_data = transf.get_transformed_data()

    ti.xcom_push(key='json_data', value=json_data)

def carregamento(ti: TaskInstance = None):
    json_data = ti.xcom_pull(key='json_data', task_ids='transformacao_tabs_json')
    
    load.atualizar_documento(
        Variable.get("FIRESTORE_COLLECTION_NAME"),
        Variable.get("FIRESTORE_DOCUMENT_ID"),
        json_data
    )


with DAG(
    'fraldas_otto_teste',
    default_args={
        'owner': 'airflow',
        'start_date': days_ago(1),
        'retries': 1
    },
    schedule_interval='@daily',
    catchup=False
):

    download_task = PythonOperator(
        task_id='extracao_tabs_g_sheets',
        python_callable=extracao
    )

    transform_task = PythonOperator(
        task_id='transformacao_tabs_json',
        python_callable=transformacao,
        op_kwargs={'data_execucao': '{{ logical_date }}'}
    )

    save_task = PythonOperator(
        task_id='carregamento_db',
        python_callable=carregamento
    )

    download_task >> transform_task >> save_task