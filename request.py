from pymongo import MongoClient
from Flask import Flask, jsonify, request
from bson.objects import ObjectID

#Conexão

client = MongoClient("mongodb://admin:admin@localhost:27017/")

db = client['mydb']

collection = db['products']

app = Flask(__name__)

@app.route("/api/products", methods=["GET"])
def listar_documentos():

    documentos = collection.find()

    resultado = []

    for documento in documentos:

        documento["_id"] = str(resultado["_id"]) # Convete o Objeto

        resultado.append(documento)

    return jsonify(resultado), 200


#Roda a aplicação Flask
if __name__ == "__main__":

    app.run(debug = True)