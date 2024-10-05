from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from datetime import datetime

from include.gsheettab import GSheetTab
from include.transform import Transform
from include.load import Load


load = Load()
gsheet = GSheetTab(Variable.get("ID_G_SHEET"))

def extracao(**context):
    df_ganhadas = gsheet.download_tab(Variable.get("ID_TAB_G_SHEET_GANHADAS"))
    df_compradas = gsheet.download_tab(Variable.get("ID_TAB_G_SHEET_COMPRADAS"))
    df_utilizadas = gsheet.download_tab(Variable.get("ID_TAB_G_SHEET_UTILIZADAS"))

    context['ti'].xcom_push(key=f'dataframe_ganhadas', value=df_ganhadas)
    context['ti'].xcom_push(key=f'dataframe_compradas', value=df_compradas)
    context['ti'].xcom_push(key=f'dataframe_utilizadas', value=df_utilizadas)

def transformacao(**context):
    json_data = {}

    df_ganhadas = context['ti'].xcom_pull(key=f'dataframe_ganhadas', task_ids='extracao_tabs_g_sheets')
    df_compradas = context['ti'].xcom_pull(key=f'dataframe_compradas', task_ids='extracao_tabs_g_sheets')
    df_utilizadas = context['ti'].xcom_pull(key=f'dataframe_utilizadas', task_ids='extracao_tabs_g_sheets')

    transf = Transform(df_ganhadas, df_compradas,df_utilizadas)
    json_data = transf.get_transformed_data()

    context['ti'].xcom_push(key='json_data', value=json_data)

def carregamento(**context):
    json_data = context['ti'].xcom_pull(key='json_data', task_ids='transformacao_tabs_json')
    
    load.atualizar_documento(
        Variable.get("FIRESTORE_COLLECTION_NAME"),
        Variable.get("FIRESTORE_DOCUMENT_ID"),
        json_data
    )


with DAG(
    'fraldas_otto_teste',
    default_args={
        'owner': 'airflow',
        'start_date': datetime(2024, 9, 26),
        'retries': 1
    },
    schedule_interval='@daily',
    catchup=False
) as dag:

    download_task = PythonOperator(
        task_id='extracao_tabs_g_sheets',
        python_callable=extracao,
        provide_context=True
    )

    transform_task = PythonOperator(
        task_id='transformacao_tabs_json',
        python_callable=transformacao,
        provide_context=True
    )

    save_task = PythonOperator(
        task_id='carregamento_db',
        python_callable=carregamento,
        provide_context=True
    )

    download_task >> transform_task >> save_task