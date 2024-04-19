from fastapi import FastAPI, HTTPException
from passlib.context import CryptContext
from typing import Optional
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str


app = FastAPI()

# Usaremos este exemplo apenas para fins de demonstração.
# Em um ambiente de produção, você deve armazenar as senhas de forma segura,
# como usando hash e salt.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configurações do JWT
SECRET_KEY = "2ce0debf73bd7ad94096a00ab1b4186c0869e6425f32c54cc6d749c6effeafae"
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

# Rota para registro de usuários
@app.post("/register/")
async def register_user(user: User):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = pwd_context.hash(user.password)
    fake_users_db[user.username] = {"username": user.username, "password": hashed_password}
    return {"message": "User registered successfully"}

# Rota para login de usuários
@app.post("/login/")
async def login_user(user: User):
    if user.username not in fake_users_db:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    stored_user = fake_users_db[user.username]
    if not verify_password(user.password, stored_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
