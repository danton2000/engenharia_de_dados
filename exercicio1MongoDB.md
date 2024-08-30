
## Com o ambiente Docker, utilizando imagens do Mongo DB

### Exercícios Práticos com MongoDB

#### 1. **Exercício de Operações Básicas com Documentos**

**Objetivo:** Aprender como inserir, consultar, atualizar e deletar documentos no MongoDB.

- **Passo 1:** Conecte-se ao MongoDB usando o CLI.

  ```bash
  docker exec -it mongo_db mongosh -u admin -p admin
  ```

- **Passo 2:** Selecione (ou crie) um banco de dados chamado `mydb`.

  ```javascript
  use mydb
  ```

- **Passo 3:** Insira um documento em uma coleção chamada `customers`.

  ```javascript
  db.customers.insertOne({ name: "Alice", age: 30, city: "New York" })
  ```

- **Passo 4:** Insira múltiplos documentos de uma vez.

  ```javascript
  db.customers.insertMany([
    { name: "Bob", age: 25, city: "Los Angeles" },
    { name: "Charlie", age: 35, city: "Chicago" }
  ])
  ```

- **Passo 5:** Consulte todos os documentos na coleção.

  ```javascript
  db.customers.find().pretty()
  ```

- **Passo 6:** Atualize um documento específico.

  ```javascript
  db.customers.updateOne(
    { name: "Alice" },
    { $set: { age: 31 } }
  )
  ```

- **Passo 7:** Delete um documento da coleção.

  ```javascript
  db.customers.deleteOne({ name: "Charlie" })
  ```

#### 2. **Exercício de Consultas com Filtros**

**Objetivo:** Aprender como realizar consultas mais complexas usando filtros no MongoDB.

- **Passo 1:** Insira documentos adicionais na coleção `customers`.

  ```javascript
  db.customers.insertMany([
    { name: "David", age: 22, city: "New York" },
    { name: "Eve", age: 28, city: "San Francisco" },
    { name: "Frank", age: 40, city: "Chicago" }
  ])
  ```

- **Passo 2:** Consulte documentos onde a idade é maior que 25.

  ```javascript
  db.customers.find({ age: { $gt: 25 } }).pretty()
  ```

- **Passo 3:** Consulte documentos onde a cidade é "New York" ou "Chicago".

  ```javascript
  db.customers.find({ city: { $in: ["New York", "Chicago"] } }).pretty()
  ```

- **Passo 4:** Consulte documentos onde a idade está entre 30 e 40.

  ```javascript
  db.customers.find({ age: { $gte: 30, $lte: 40 } }).pretty()
  ```

#### 3. **Exercício de Indexação**

**Objetivo:** Aprender como criar índices para melhorar a performance de consultas no MongoDB.

- **Passo 1:** Crie um índice em um campo.

  ```javascript
  db.customers.createIndex({ age: 1 })
  ```

- **Passo 2:** Verifique os índices criados na coleção.

  ```javascript
  db.customers.getIndexes()
  ```

- **Passo 3:** Execute uma consulta usando o índice criado.

  ```javascript
  db.customers.find({ age: { $gte: 30 } }).explain("executionStats")
  ```

#### 4. **Exercício de Operações com Arrays**

**Objetivo:** Manipular e consultar documentos com arrays.

- **Passo 1:** Insira documentos com arrays.

  ```javascript
  db.products.insertMany([
    { name: "Laptop", tags: ["electronics", "computer"], price: 1200 },
    { name: "Smartphone", tags: ["electronics", "phone"], price: 800 },
    { name: "Tablet", tags: ["electronics", "computer", "portable"], price: 600 }
  ])
  ```

- **Passo 2:** Consulte documentos que contêm um determinado valor no array.

  ```javascript
  db.products.find({ tags: "computer" }).pretty()
  ```

- **Passo 3:** Consulte documentos onde o array possui exatamente um conjunto de valores.

  ```javascript
  db.products.find({ tags: { $all: ["electronics", "computer"] } }).pretty()
  ```

- **Passo 4:** Adicione um valor ao array de um documento específico.

  ```javascript
  db.products.updateOne(
    { name: "Laptop" },
    { $addToSet: { tags: "high-end" } }
  )
  ```

#### 5. **Exercício de Agregação**

**Objetivo:** Usar a framework de agregação para processar dados de maneiras complexas.

- **Passo 1:** Use uma agregação para calcular a média dos preços dos produtos.

  ```javascript
  db.products.aggregate([
    { $group: { _id: null, avgPrice: { $avg: "$price" } } }
  ])
  ```

- **Passo 2:** Use uma agregação para contar quantos produtos têm a tag "electronics".

  ```javascript
  db.products.aggregate([
    { $match: { tags: "electronics" } },
    { $count: "numElectronics" }
  ])
  ```

- **Passo 3:** Agregue e ordene os produtos pelo preço em ordem decrescente.

  ```javascript
  db.products.aggregate([
    { $sort: { price: -1 } }
  ])
  ```

#### 6. **Exercício de Operações com Subdocumentos**

**Objetivo:** Trabalhar com documentos que contêm subdocumentos.

- **Passo 1:** Insira documentos com subdocumentos.

  ```javascript
  db.orders.insertMany([
    {
      order_id: 1,
      customer: { name: "Alice", address: "123 Maple St" },
      items: [
        { product: "Laptop", quantity: 1, price: 1200 },
        { product: "Tablet", quantity: 2, price: 600 }
      ]
    },
    {
      order_id: 2,
      customer: { name: "Bob", address: "456 Oak St" },
      items: [
        { product: "Smartphone", quantity: 3, price: 800 },
        { product: "Laptop", quantity: 1, price: 1200 }
      ]
    }
  ])
  ```

- **Passo 2:** Consulte documentos onde o nome do cliente é "Alice".

  ```javascript
  db.orders.find({ "customer.name": "Alice" }).pretty()
  ```

- **Passo 3:** Atualize o endereço de um cliente específico.

  ```javascript
  db.orders.updateOne(
    { "customer.name": "Alice" },
    { $set: { "customer.address": "789 Birch St" } }
  )
  ```

#### 7. **Exercício de Operações de Texto**

**Objetivo:** Trabalhar com índices de texto para realizar buscas textuais.

- **Passo 1:** Crie um índice de texto para um campo específico.

  ```javascript
  db.products.createIndex({ name: "text" })
  ```

- **Passo 2:** Realize uma busca textual para encontrar produtos com a palavra "Laptop".

  ```javascript
  db.products.find({ $text: { $search: "Laptop" } })
  ```

- **Passo 3:** Realize uma busca textual com exclusão de palavras.

  ```javascript
  db.products.find({ $text: { $search: "Laptop -Tablet" } })
  ```

#### 8. **Exercício de Transações**

**Objetivo:** Usar transações para garantir a consistência de dados em operações múltiplas.

- **Passo 1:** Inicie uma sessão para uma transação.

  ```javascript
  const session = db.getMongo().startSession();
  session.startTransaction();
  ```

- **Passo 2:** Realize operações dentro da transação.

  ```javascript
  const customersColl = session.getDatabase("mydb").customers;
  const ordersColl = session.getDatabase("mydb").orders;

  customersColl.updateOne({ name: "Alice" }, { $set: { age: 32 } }, { session });
  ordersColl.insertOne({ order_id: 3, customer: { name: "Alice" }, items: [{ product: "Smartwatch", quantity: 1, price: 250 }] }, { session });
  ```

- **Passo 3:** Confirme (commit) ou aborte (abort) a transação.

  ```javascript
  session.commitTransaction();
  session.endSession();
  ```

#### 9. **Exercício de Operações com Geoespacial**

**Objetivo:** Usar operadores geoespaciais para trabalhar com dados de localização.

- **Passo 1:** Insira documentos com coordenadas de localização.

  ```javascript


  db.places.insertMany([
    { name: "Central Park", location: { type: "Point", coordinates: [-73.968285, 40.785091] } },
    { name: "Empire State Building", location: { type: "Point", coordinates: [-73.985656, 40.748817] } }
  ])
  ```

- **Passo 2:** Crie um índice geoespacial.

  ```javascript
  db.places.createIndex({ location: "2dsphere" })
  ```

- **Passo 3:** Realize uma busca de proximidade geoespacial.

  ```javascript
  db.places.find({
    location: {
      $near: {
        $geometry: { type: "Point", coordinates: [-73.985656, 40.748817] },
        $maxDistance: 5000
      }
    }
  })
  ```

