from fastapi import FastAPI, HTTPException
from passlib.context import CryptContext
from typing import Optional
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import BaseModel
import asyncpg
import os

# Definição do modelo de usuário
class User(BaseModel):
    username: str
    password: str
    phone: str = None
    postalcode: str = None
    usertype: str = None


app = FastAPI()

# Usaremos este exemplo apenas para fins de demonstração.
# Em um ambiente de produção, você deve armazenar as senhas de forma segura,
# como usando hash e salt.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configurações do banco de dados
DATABASE_URL = os.environ.get("PGURL", "postgres://postgres:postgres@db:5432/agendinha") 
# Configurações do JWT
SECRET_KEY = os.environ.get("SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Simulando um banco de dados
fake_users_db = {}

# Função para verificar a senha
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Função para gerar o token JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Função para conectar ao banco de dados
async def get_database():
    return await asyncpg.connect(DATABASE_URL)

# Rota para resetar o banco de dados
@app.post("/api/v1/db-reset/")
async def reset_database():
    try:
        # Conecta ao banco de dados
        conn = await get_database()
        # Executa as operações para resetar o banco de dados
        await conn.execute("DROP TABLE IF EXISTS users;")
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(100) NOT NULL,
                phone VARCHAR(20),
                postalcode VARCHAR(10),
                usertype VARCHAR(20)
            );
        """)
        # Fecha a conexão com o banco de dados
        await conn.close()
        return {"message": "Database reset successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reset database: {str(e)}")

# Função para verificar se um usuário já existe
async def user_exists(username: str):
    conn = await get_database()
    try:
        query = """
            SELECT 1 FROM "users" WHERE username = $1
        """
        result = await conn.fetchrow(query, username)   
        # Verifica se o resultado é None
        await conn.close()
        return result is not None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to check if user exists: {str(e)}")

# Função para registrar um usuário
@app.post("/api/v1/register/")
async def register_user(user: User):
    try:
        conn = await get_database()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to database: {str(e)}")
    
    # Verifica se o usuário já existe
    if await user_exists(user.username):
        raise HTTPException(status_code=400, detail="User already exists")
        
    try:
        # Hash da senha antes de inserir no banco de dados
        hashed_password = pwd_context.hash(user.password)
        
        # Insere o usuário no banco de dados
        query = """
            INSERT INTO "users" (username, password, phone, postalcode, usertype)
            VALUES ($1, $2, $3, $4, $5)
        """
        await conn.execute(query, user.username, hashed_password, user.phone, user.postalcode, user.usertype)
        
        # Fecha a conexão com o banco de dados
        await conn.close()
        
        return {"message": "User registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to register user: {str(e)}")


# Função para autenticar um usuário
@app.post("/api/v1/login/")
async def login_user(user: User):
    try:
        # Conecta ao banco de dados
        conn = await get_database()
        query = """
            SELECT * FROM "users" WHERE username = $1
        """
        record = await conn.fetchrow(query, user.username)
        if record is None:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        stored_password = record["password"]
        if not pwd_context.verify(user.password, stored_password):
            raise HTTPException(status_code=401, detail="Invalid username or password")
        access_token = create_access_token(data={"sub": user.username})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")
    return {"access_token": access_token, "token_type": "bearer"}

# função para healthcheck
@app.get("/api/v1/healthcheck/")
async def healthcheck():
    return {"status": "ok"}