from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from typing import Optional
from jose import JWTError, jwt
from datetime import datetime, timedelta
import asyncpg
import os
from model import User, UserBase, UserLogin


app = FastAPI()

# Adicione o middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# Rota para resetar o banco de dados
@app.post("/api/v1/db-reset/")
async def reset_database():
    from dao import Database
    await Database.reset_database()
    return {"message": "Database reset successfully"}

# Função para registrar um usuário
@app.post("/api/v1/register/")
async def register_user(user: UserBase):
    from dao import UserDAO
    result = await UserDAO.insert(user)
    
    if result is not None:
        return {"message": "User registered successfully"}

# Função para autenticar um usuário
@app.post("/api/v1/login/")
async def login_user(user: UserLogin):
    try:
        from dao import UserDAO
        record = await UserDAO.get_password(user.email)

        if record is None:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        stored_password = record["password"]
        if not pwd_context.verify(user.password, stored_password):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        access_token = create_access_token(data={"sub": user.email})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")
    return {"access_token": access_token, "token_type": "bearer"}

# função para healthcheck
@app.get("/")
async def healthcheck():
    return {"status": "ok"}