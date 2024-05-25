# app-backend
[![Running Tests](https://github.com/Agendinha/app-backend/actions/workflows/test.yaml/badge.svg)](https://github.com/Agendinha/app-backend/actions/workflows/test.yaml)

Para rodar a API localmente, você precisa executar o script Python que contém sua aplicação FastAPI.

```bash
uvicorn main:app --reload
```

Isso iniciará o servidor Uvicorn e sua aplicação FastAPI. O parâmetro `--reload` faz com que o servidor reinicie automaticamente sempre que você fizer alterações no código-fonte, o que é útil durante o desenvolvimento.

Depois de iniciar o servidor, você poderá acessar sua API em `http://localhost:8000`. Se você seguiu o exemplo anterior, a documentação interativa (Swagger UI) estará disponível em `http://localhost:8000/docs`, onde você pode explorar e testar os endpoints da sua API.

Certifique-se de que nenhuma outra aplicação esteja ocupando a porta 8000 em seu sistema, pois isso pode causar conflitos. Se necessário, você pode alterar a porta usando o argumento `--port` ao iniciar o servidor.

Se você tiver qualquer problema ou dúvida ao rodar a API localmente, não hesite em perguntar!

# docker-compose

Para rodar a API localmente com o Docker, você pode executar o seguinte comando no terminal partindo da raiz da aplicação, ou seja, no diretório `app-backend`.:
    
```bash
docker-compose up --build
```

# database

para conectar ao banco de dados. 

```bash
source .env.sh
```

Nota: para usar o banco de dados, você deve ter o arquivo `.env.sh` criado. E rodar o projeto localmente.