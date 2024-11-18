# Depedencias do aiflow
from airflow import DAG
from airflow.operators.python import PythonOperator, get_current_context
from airflow.macros import ds_add
from os.path import join
import pendulum
import os
import boto3
import requests
import pandas as pd
from io import StringIO

with DAG (
    
    # Sobre essa dag
    "airflow_clima_1",
    start_date=pendulum.datetime(2024,10,29, tz = "UTC"),
    # schedule_interval='0 0 * * 1' = TODA TERÇA-FEIRA, crontab guru
    schedule_interval='0 0 * * 2'
    
) as dag:
    # Tudo que essa DAG irá executar
    
    #client minio
    #boto3 api de  acesso
    s3 = boto3.client (
        
        's3',
        region_name = 'us-east-1',
        endpoint_url = os.environ.get('MINIO_ENDPOINT'),
        aws_access_key_id = os.environ.get('MINIO_ACCESS_KEY'),
        aws_secret_access_key = os.environ.get('MINIO_SECRET_KEY')
        
    )
    
    # Função do python
    def extract_data(city, data_interval_end):
        # consegue ver os prints na aba de logs
        # print(city)
        # print(data_interval_end)
        
        key = "TRTF82LWADE2ZWAY2HAQXBZWY"
        
        URL = join('https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/',
            f'{city}/{data_interval_end}/{ds_add(data_interval_end, 7)}?unitGroup=metric&include=days&key={key}&contentType=csv')
        
        req = requests.get(URL, verify  = False)
        
        #temp_file = "/opt/airflow/output/dados.csv"
        filename = f'dados_clima_{city}_{data_interval_end}_{ds_add(data_interval_end, 7)}.csv'
        
        # Escrevendo no arquivo o que o request retornou
        # with open(temp_file, "w") as text:
            
        # text.write(req.text)
        # Criando o arquivo
        s3.put_object(
            # O que vamos salvar
            Body = req.text,
            # Onde vamos armazenas
            Bucket = 'bronze',
            # O arquivo
            Key = filename,
            # Tipo do arquivo
            ContentType = 'application/csv'
            
        )
        
        # pegando o contexto desta execução
        context = get_current_context()
    
        ti = context["ti"]
        # adicionar valor no xcom
        # nome do arquivo ele vai salvar no xcom para a proxima tarefa poder capturar essa informação
        ti.xcom_push(key = 'file', value=filename) 
        
     
    def clean_data(source):
        # source = nome do arquivo que a task utilizou(processou)
        #print(f'Rodando task de limpeza de dados bi arquivo: {source}')
        
        # ler o arquivo
        read_file = s3.get_object (
            # local
            Bucket =  'bronze',
            # arquivo
            Key = source
            
        )
        
        data = pd.read_csv(read_file['Body'],  sep = ',')
        
        # Criando um buffer, para salver o arquivo em csv
        csv_buffer = StringIO()
        
        # Pegando algumas colunas
        # Salva esse objeto
        data[['name', 'datetime', 'tempmin', 'temp', 'tempmax']].to_csv(csv_buffer, index=False)
        
        s3.put_object (
            # O que vamos salvar, o que tem nesse buffer
            Body = csv_buffer.getvalue(),
            # Onde vamos armazenas
            Bucket = 'silver',
            # O arquivo
            Key = f"cleansed_{source}",
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
    
    clean_weather_data = PythonOperator(
        # nome da tarefa(task)
        task_id = 'clean_weather_data',
        # nome da função
        python_callable = clean_data,
        # argumentos
        # Puxando uma informação da task get_weather_data, e colocando como argumento
        op_kwargs = {
            'source': "{{ti.xcom_pull(task_ids='get_weather_data', key='file')}}"
            }
    )
        
    # O que eu quero rodar na minha DAG
    # task >>(proxima) taks
    get_weather_data >> clean_weather_data