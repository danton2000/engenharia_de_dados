

### 1. **Instalando o Docker no Windows**
Antes de começarmos, precisamos instalar o Docker.

#### Passo a Passo:
- Acesse o site do Docker: [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop).
- Baixe o **Docker Desktop para Windows**.
- Durante a instalação, certifique-se de habilitar a opção "Use the WSL 2 based engine".
- Siga as instruções de instalação e reinicie o computador se necessário.
- Após a instalação, abra o **Docker Desktop**.

Para verificar se tudo está funcionando corretamente, abra o terminal (PowerShell ou CMD) e execute o seguinte comando:
```bash
docker --version
```
Você deve ver a versão do Docker instalada.

Para verificar se a engine do Docker está no ar, execute o seguinte comando:

```bash
docker ps
````

Caso mostre a mensagem `Cannot connect to the Docker daemon at unix:///Users/seu_usuario/.docker/run/docker.sock. Is the docker daemon running?` verifique se o **Docker Desktop** está ativo, caso contrário inicialize ele.

### 2. **Executando Containers Prontos com `docker run`**
Agora vamos rodar um container com uma imagem já existente no [Docker Hub](https://hub.docker.com). 

#### Exemplo 1: Rodando o container do **PostgreSQL**
O PostgreSQL é um banco de dados amplamente utilizado em engenharia de dados que possui uma imagem oficial no Docker Hub chamada `postgres`.

Comando para baixar e rodar o container:
```bash
docker run --name meu_postgres -e POSTGRES_PASSWORD=password -e POSTGRES_USER=user -d postgres
```
Aqui estamos:
- Usando `docker run` para criar e rodar um container.
- `--name meu_postgres` dá um nome ao container.
- `-e POSTGRES_PASSWORD=password` define uma variável de ambiente para a senha do PostgreSQL.
- `-e POSTGRES_USER=user` define uma variável de ambiente para o usuário do PostgreSQL.
- `-d` executa o container em segundo plano.
- `postgres` é a imagem oficial do PostgreSQL.

Verificando se o container está rodando:
```bash
docker ps
```
Uma forma de acessar a console do Postgres nesse exemplo é com o docker exec (após executar o comando abaixo ele irá solicitar a senha definida na variável `POSTGRES_USER`:

```bash
docker exec -it meu_postgres psql -Uuser -W
```

Ou utilizando o client de sua preferência como o `pgAdmin` ou o `dBeaver`.

Para encerrar a execução do container execute o comando:

```bash
docker stop meu_postgres
````

E para deletar o container:

```bash
docker rm meu_postgres
```

#### Exemplo 2: Rodando o container do **Jupyter Notebook**
O Jupyter é útil para manipulação de dados, utilizando Python.

Comando:
```bash
docker run -p 8888:8888 jupyter/minimal-notebook
```
Aqui estamos:
- `-p 8888:8888` mapeando a porta 8888 do container para a porta 8888 do host, para acessar o Jupyter no navegador.

Abra o navegador e vá para: `http://localhost:8888`.

### 3. **Criando um Dockerfile Simples**
Um **Dockerfile** permite criar sua própria imagem de container.

#### Exemplo: Dockerfile para rodar um script Python

1. Crie um diretório no seu computador para o projeto, ex: `meu_projeto`.
2. Dentro dessa pasta, crie um arquivo chamado `Dockerfile` (sem extensão) e cole o seguinte conteúdo:

```Dockerfile
# Usando uma imagem base do Python
FROM python:3.8-slim

# Definindo o diretório de trabalho dentro do container
WORKDIR /app

# Copiando o arquivo de script para o container
COPY script.py /app

# Definindo o comando que será executado ao rodar o container
CMD ["python", "script.py"]
```

3. Na mesma pasta, crie o arquivo `script.py` com o seguinte conteúdo:
```python
print("Olá, Docker!")
```

4. No terminal, navegue até a pasta do projeto e execute o seguinte comando para construir a imagem:
```bash
docker build -t meu_python_app .
```

5. Agora, execute o container:
```bash
docker run meu_python_app
```

Você verá a saída:
```
Olá, Docker!
```

### 4. **Usando o `docker-compose`**
O **docker-compose** permite rodar múltiplos containers de forma coordenada. Poderíamos executar os container abaixo com os comandos `docker run --name meu_postgres -e POSTGRES_PASSWORD=password -e POSTGRES_USER=user -d postgres` e `docker run -p 5050:80 -e PGADMIN_DEFAULT_EMAIL=admin@admin.com -e PGADMIN_DEFAULT_PASSWORD=admin dpage/pgadmin4` que ele irá rodar da mesma forma, mas optamos por criar um arquivo docker-compose.yml para **facilitar** a gestão dos containers

#### Exemplo: Configurando PostgreSQL e PGAdmin com `docker-compose`

1. Crie um diretório para o projeto, ex: `meu_banco_de_dados`.
2. Dentro da pasta, crie um arquivo `docker-compose.yml` com o seguinte conteúdo:

```yaml
services:
  db:
    container_name: meu_postgres
    image: postgres
    restart: always
    environment:
      POSTGRES_PASSWORD: password
      POSTGRES_USER: user

  pgadmin:
    image: dpage/pgadmin4
    restart: always
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@admin.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "5050:80"
```

3. Para subir os todos containers do docker-compose, execute:
```bash
docker-compose up -d
```

4. Para subir apenas um container podemos executar:
```bash
docker-compose up -d pgadmin
```


Agora você tem o PostgreSQL rodando, e pode acessar o PGAdmin no navegador através do endereço: `http://localhost:5050` com o login `admin@admin.com` e a senha `admin`.

### 5. **Comandos Úteis do Docker**
- **Ver containers rodando**: 
  ```bash
  docker ps
  ```
- **Parar um container**:
  ```bash
  docker stop nome_do_container
  ```
- **Remover um container**:
  ```bash
  docker rm nome_do_container
  ```
- **Ver imagens disponíveis**:
  ```bash
  docker images
  ```
- **Remover uma imagem**:
  ```bash
  docker rmi nome_da_imagem
  ```
