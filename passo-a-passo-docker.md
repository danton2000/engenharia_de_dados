1 - ACESSAR A PASTA COM AS CONFIGS DO DOCKER
2 - INSTALAR OS CONTAINER/IMAGENS NESSA PASTA
3 - Execuntado dentro do container(MYSQL):  docker exec -it mysql_db bash
	- EXECUTANDO DENTRO DO CONTAINER(MONGODB): docker exec -it mongodb bash
4 - EXECUTANDO DENTRO DO MYSQL:  mysql -uuser -ppassword
	- EXECUTANDO DENTRO DO MONGODB: mongosh -u admin -p admin
5 - ESCOLHENDO O BANCO DE DADOS: USE NOME_BANCO;
6 - VISUALIZANDO AS TABELAS DO BANCO DE DADOS ESCOLHIDO: SHOW TABLES;
7 - CRIANDO UM BANCO NO MONGODB: use mydb
8 - CRIANDO UMA COLLECTION:  db.createCollection('products');
9 - INSERINDO VALORES NA COLLECTION:  db.products.insertOne({name: 'Mouse', price: 100})
10 - VISUALIZANDO OS DADOS DA COLLECTION: db.products.find()
11 - ATUALIZANDO UM REGISTRO COM O MONGODB:  db.products.updateOne({name: 'Monitor'}, {$set:{price: 1600}});

--
docker compose up -d redis
docker exec -it redis_db redis-cli
SET user:2 "Daniel"
GET user:2
LPUSH tasks "task1" "task2" "task3"
LPUSH tasks "task1"