import pymongo
import mysql.connector
from mysql.connector import Error

url = "mongodb://admin:admin@localhost:27017"
mongo_client = pymongo.MongoClient(url)
mongo_db = mongo_client["mydb"]
mongo_collection = mongo_db["products"]

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
            price DECIMAL(10, 2),
            stock INT
        )
        """)
        print("Tabela 'products' criada no MySQL (se não existia).")

        # Limpar a tabela para evitar duplicatas durante o teste
        mysql_cursor.execute("DELETE FROM products")

except Error as e:
    print(f"Erro ao conectar ao MySQL: {e}")


def transfer_mongo_to_mysql():
    try:
        documents = mongo_collection.find()
        for doc in documents:
            sql = "INSERT INTO products (name, price, stock) VALUES (%s, %s, %s)"
            values = (doc["name"], doc["price"], doc["stock"])
            mysql_cursor.execute(sql, values)
        mysql_conn.commit()
        print("Dados transferidos do MongoDB para o MySQL.")
    except Exception as e:
        print(f"Erro ao transferir dados: {e}")

# Transferir dados do MySQL para o MongoDB
def transfer_mysql_to_mongo():
    try:
        mysql_cursor.execute("SELECT name, price, stock FROM products")
        rows = mysql_cursor.fetchall()
        for row in rows:
            mongo_collection.insert_one({"name": row[0], "price": float(row[1]), "stock": row[2]})
        print("Dados transferidos do MySQL para o MongoDB.")
    except Exception as e:
        print(f"Erro ao transferir dados: {e}")


if __name__ == '__main__':
    print("ok")
    transfer_mongo_to_mysql()
    transfer_mysql_to_mongo()

    mongo_collection.insert_many([
       {"name": "Laptop", "price": 1200.0, "stock": 50},
       {"name": "Smartphone", "price": 800.0, "stock": 200},
       {"name": "Tablet", "price": 400.0, "stock": 100}
    ])

    mongo_collection.insert_one({"name": "Monitor", "price": 1200.0, "stock": 50})
