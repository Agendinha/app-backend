from fastapi import HTTPException
from model.user import User
from passlib.context import CryptContext
import asyncpg
import os

# Usaremos este exemplo apenas para fins de demonstração.
# Em um ambiente de produção, você deve armazenar as senhas de forma segura,
# como usando hash e salt.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserDAO:
    @staticmethod
    async def insert(user: User):
        conn = await get_database()
        if await UserDAO.exists(user.email, conn):
            raise HTTPException(status_code=400, detail="User already exists")

        # Hash da senha antes de inserir no banco de dados
        hashed_password = pwd_context.hash(user.password)

        try:
            query = """
                INSERT INTO "user" (email, username, password, usertype)
                VALUES ($1, $2, $3, $4)
            """
            async with conn.transaction():
                result = await conn.execute(query, user.email, user.username, hashed_password, user.usertype)
                return result
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to insert user: {str(e)}")
        finally:
            await conn.close()

    @staticmethod
    async def exists(email: str, conn):
        try:
            query = """
                SELECT 1 FROM "user" WHERE email = $1
            """
            result = await conn.fetchval(query, email)
            return result is not None
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to check if user exists: {str(e)}")

    @staticmethod
    async def get(email: str = None, id: int = None):
        conn = await get_database()
        try:
            query = """
                SELECT * FROM "user" WHERE email = $1 OR id = $2
            """
            result = await conn.fetch(query, email, id)
            return result
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get user: {str(e)}")
        finally:
            await conn.close()

    @staticmethod
    async def delete(id: int):
        conn = await get_database()
        try:
            query = """
                DELETE FROM "user" WHERE id = $1
            """
            result = await conn.execute(query, id)
            return result
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete user: {str(e)}")
        finally:
            await conn.close()

    @staticmethod
    async def get_password(email: str):
        conn = await get_database()
        try:
            query = """
                SELECT password FROM "user" WHERE email = $1
            """
            result = await conn.fetchval(query, email)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get password: {str(e)}")
        finally:
            await conn.close()

# Função para conectar ao banco de dados
async def get_database():
    DATABASE_URL = os.environ.get("PGURL", "postgres://postgres:postgres@db:5432/agendinha") 
    return await asyncpg.connect(DATABASE_URL)
