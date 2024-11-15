# Depedencias do aiflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.macros import ds_add
from os.path import join
import pendulum
import os
import boto3
import requests


with DAG (
    
    # Sobre essa dag
    "airflow_clima_1",
    start_date=pendulum.datetime(2024,10,29, tz = "UTC"),
    # schedule_interval='0 0 * * 1' = TODA TERÇA-FEIRA, crontab guru
    schedule_interval='0 0 * * 2'
    
) as dag:
    # Tudo que essa DAG irá executar
    
    # Função do python
    def extract_data(city, data_interval_end):
        # consegue ver os prints na aba de logs
        # print(city)
        # print(data_interval_end)
        
        key = "TRTF82LWADE2ZWAY2HAQXBZWY"
        
        #client minio
        #boto3 api de  acesso
        s3 = boto3.client (
            
            's3',
            region_name = 'us-east-1',
            endpoint_url = os.environ.get('MINIO_ENDPOINT'),
            aws_access_key_id = os.environ.get('MINIO_ACCESS_KEY'),
            aws_secret_access_key = os.environ.get('MINIO_SECRET_KEY')
            
        )
        
        URL = join('https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/',
            f'{city}/{data_interval_end}/{ds_add(data_interval_end, 7)}?unitGroup=metric&include=days&key={key}&contentType=csv')
        
        req = requests.get(URL, verify  = False)
        
        temp_file = "/opt/airflow/output/dados.csv"
        
        # Escrevendo no arquivo o que o request retornou
        # with open(temp_file, "w") as text:
            
        #     text.write(req.text)
        
        s3.put_object(
            # O que vamos salvar
            Body = req.text,
            # Onde vamos armazenas
            Bucket = 'bronze',
            # O arquivo
            Key = f'dados_clima_{city}_{data_interval_end}_{ds_add(data_interval_end, 7)}.csv',
            # Tipo do arquivo
            ContentType = 'application/csv'
            
        )
    
    # "Função" do airflow
    get_weather_data = PythonOperator(
        # nome da tarefa(task)
        task_id = 'get_weather_data',
        # nome da função
        python_callable = extract_data,
        # argumentos
        op_kwargs = {
            'city': 'PortoAlegre',
            'data_interval_end': '{{data_interval_end.strftime("%Y-%m-%d")}}'
            }
    )
        
    # O que eu quero rodar na minha DAG
    get_weather_data