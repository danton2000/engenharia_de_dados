# Usando a imagem base do Python 3.8
FROM python:3.8-slim

# Definindo o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiando o arquivo de script Python para o contêiner
COPY script.py .

# Instalando dependências (se houver)
#RUN pip install --no-cache-dir requests
RUN pip install "apache-airflow==2.10.2" apache-airflow-providers-google==10.1.0
RUN pip install --no-cache-dir pendulum

# Definindo o comando de execução padrão
#CMD ["python", "script.py"]

# Definindo o comando de execução padrão
CMD ["python", "airflow_demo_1.py"]
