from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from passlib.context import CryptContext
from typing import Optional
from jose import jwt
from datetime import datetime, timedelta
import os
from model.user import UserBase, UserLogin
from dao.user import UserDAO
from dao.database import Database

from typing import List
from model.schedule import ScheduleBase, ScheduleCreate, ScheduleUpdate  # Importar os modelos de schedule
from dao.schedule import ScheduleDAO  # Importar o DAO de schedule


appServer = FastAPI()

# Adicione o middleware CORS
appServer.add_middleware(
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
@appServer.post("/api/v1/db-reset/")
async def reset_database():
    await Database.reset_database()
    return {"message": "Database reset successfully"}

# Função para registrar um usuário
@appServer.post("/api/v1/register/")
async def register_user(user: UserBase):
    result = await UserDAO.insert(user)
    
    if result is not None:
        try:
            user = await UserDAO.get(email=user.email)
            user = user[0]
            #remove password from response
            user = {key: value for key, value in user.items() if key != "password"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get user: {str(e)}")
        return {"message": "User registered successfully", "user": user}

# Função para autenticar um usuário
@appServer.post("/api/v1/login/")
async def login_user(user: UserLogin):
    try:
        record = await UserDAO.get_password(user.email)

        if record is None:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        stored_password = record

        if not pwd_context.verify(user.password, stored_password):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        access_token = create_access_token(data={"sub": user.email})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")
    #pick username, usertype and id
    try:
        user = await UserDAO.get(email=user.email)
        user = user[0]
        #remove password from response
        user = {key: value for key, value in user.items() if key != "password"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user: {str(e)}")

    return {"access_token": access_token, "token_type": "bearer", "user": user}

# função para healthcheck
@appServer.get("/")
async def healthcheck():
    return {"status": "ok"}

@appServer.post("/api/v1/schedules/", response_model=ScheduleBase)
async def create_schedule(schedule: ScheduleCreate):
    result = await ScheduleDAO.insert(schedule)
    if result is None:
        raise HTTPException(status_code=400, detail="Error creating schedule")
    return result

@appServer.get("/api/v1/schedules/", response_model=List[ScheduleBase])
async def get_schedules():
    schedules = await ScheduleDAO.get_all()
    return schedules

@appServer.get("/api/v1/schedules/{schedule_id}", response_model=ScheduleBase)
async def get_schedule(schedule_id: int):
    schedule = await ScheduleDAO.get(schedule_id)
    if schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule

@appServer.put("/api/v1/schedules/{schedule_id}", response_model=ScheduleBase)
async def update_schedule(schedule_id: int, schedule: ScheduleUpdate):
    result = await ScheduleDAO.update(schedule_id, schedule)
    if result is None:
        raise HTTPException(status_code=400, detail="Error updating schedule")
    return result

@appServer.delete("/api/v1/schedules/{schedule_id}")
async def delete_schedule(schedule_id: int):
    result = await ScheduleDAO.delete(schedule_id)
    if not result:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return {"message": "Schedule deleted successfully"}