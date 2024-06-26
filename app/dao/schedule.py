from fastapi import HTTPException
from model.schedule import ScheduleCreate, ScheduleUpdate, ScheduleBase
import asyncpg
import os
from datetime import datetime

class ScheduleDAO:
    @staticmethod
    async def insert(schedule: ScheduleCreate):
        conn = await get_database()
        try:
            # Convertendo o start_time para uma instância de datetime sem informação de fuso horário
            start_time = schedule.start_time.replace(tzinfo=None)

            query = """
                INSERT INTO schedule (customer_id, username, service, start_time)
                VALUES ($1, $2, $3, $4)
                RETURNING id, customer_id, username, service, start_time
            """
            async with conn.transaction():
                record = await conn.fetchrow(query, schedule.customer_id, schedule.username, schedule.service, start_time)
                return ScheduleBase(**record)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to insert schedule: {str(e)}")
        finally:
            await conn.close()

    @staticmethod
    async def get_all():
        conn = await get_database()
        try:
            query = """
                SELECT id, customer_id, username, service, start_time FROM schedule
            """
            records = await conn.fetch(query)
            return [ScheduleBase(**record) for record in records]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get schedules: {str(e)}")
        finally:
            await conn.close()

    @staticmethod
    async def get(schedule_id: int):
        conn = await get_database()
        try:
            query = """
                SELECT id, customer_id, username, service, start_time FROM schedule WHERE id = $1
            """
            record = await conn.fetchrow(query, schedule_id)
            if record:
                return ScheduleBase(**record)
            else:
                raise HTTPException(status_code=404, detail="Schedule not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get schedule: {str(e)}")
        finally:
            await conn.close()

    @staticmethod
    async def update(schedule_id: int, schedule: ScheduleUpdate):
        conn = await get_database()
        try:
            update_data = schedule.dict(exclude_unset=True)
            set_clause = ", ".join([f"{key} = ${i+2}" for i, key in enumerate(update_data.keys())])
            query = f"""
                UPDATE schedule SET {set_clause} WHERE id = $1
                RETURNING id, customer_id, username, service, start_time
            """
            if "start_time" in update_data:
                update_data["start_time"] = update_data["start_time"].replace(tzinfo=None)

            values = [schedule_id] + list(update_data.values())
            async with conn.transaction():
                record = await conn.fetchrow(query, *values)
                if record:
                    return ScheduleBase(**record)
                else:
                    raise HTTPException(status_code=404, detail="Schedule not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to update schedule: {str(e)}")
        finally:
            await conn.close()

    @staticmethod
    async def delete(schedule_id: int):
        conn = await get_database()
        try:
            query = """
                DELETE FROM schedule WHERE id = $1
                RETURNING id
            """
            async with conn.transaction():
                record = await conn.fetchrow(query, schedule_id)
                if record:
                    return True
                else:
                    raise HTTPException(status_code=404, detail="Schedule not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete schedule: {str(e)}")
        finally:
            await conn.close()

# Função para conectar ao banco de dados
async def get_database():
    DATABASE_URL = os.environ.get("PGURL", "postgres://postgres:postgres@db:5432/agendinha") 
    return await asyncpg.connect(DATABASE_URL)
