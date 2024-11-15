# Passo a passo Air Flow
(https://www.youtube.com/watch?v=aBeBylG7LUU&ab_channel=BrunoFeldman)

## Instalação do Air Flow com o Docker

- https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html

- Fetching docker-compose.yaml(arquivo)

## Criar um diretorio lab-docker-airflow
## Colocar o arquivo yaml nesse diretorio
- comando para baixar a imagem: docker compose up -d
- host local do airflow http://localhost:8080/
- usuario e senha no arquivo yaml

### Criando depedencias
- arquivo: requirements.txt

### Crando um dockerfile para conter nossas imagens
- comando para desligar os containers: docker compose down
- comando para construir a imagem: docker compose build
- comando para levantar as imagens: docker compose up -d

#### Adicionando o container minio no arquivo yaml
- commando para levantar a imagem: docker compose up -d minio

### Adicionando varias de ambiente do MINIO no docker-compose
- commando para baixar a imagem: docker compose down