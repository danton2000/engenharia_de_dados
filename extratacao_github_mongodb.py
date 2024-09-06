import requests
import pymongo

import mysql.connector
from mysql.connector import Error

# Precisa ter o mongodb e o mongodb-express
# Acessar o bash do mongo, com o docker.


# Conectar ao mongo
mongo_client = pymongo.MongoClient('mongodb://admin:admin@localhost:27017/')

mongo_db = mongo_client['github_db']

mongo_collection = mongo_db["github_collection"]

try:
    mysql_conn = mysql.connector.connect(
        host='localhost',
        database='example_db',
        user='user',
        password='password'
    )

    if mysql_conn.is_connected():
        print("Conectado ao MySQL")
        mysql_cursor = mysql_conn.cursor()

        # Criar tabela no MySQL se não existir
        mysql_cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            language VARCHAR(100),
            stock VARCHAR(100)
        )
        """)
        print("Tabela 'products' criada no MySQL (se não existia).")

        # Limpar a tabela para evitar duplicatas durante o teste
        mysql_cursor.execute("DELETE FROM products")

except Error as e:
    print(f"Erro ao conectar ao MySQL: {e}")
    
if __name__ == '__main__':
    #Definir a URL da API e parametros
    url = "https://api.github.com/users/deepfakes/repos"

    #Fazer a requisição HTTP Get
    response = requests.get(url)

    items = response.json()

    for item in items:

        #print(f"{item['name']}")

        mongo_collection.insert_one({"name": item['name'], "language":  item['language'], "url": item['html_url']})

    documents = mongo_collection.find()
    for doc in documents:
        sql = "INSERT INTO products (name, language, url) VALUES (%s, %s, %s)"
        values = (doc["name"], doc["language"], doc["url"])
        mysql_cursor.execute(sql, values)
    mysql_conn.commit()
    print("Dados transferidos do MongoDB para o MySQL.")