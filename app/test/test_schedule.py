import pytest
from unittest.mock import patch, AsyncMock
from datetime import datetime
from model.schedule import ScheduleCreate, ScheduleUpdate, ScheduleBase
from dao.schedule import ScheduleDAO

@pytest.mark.asyncio
@patch("dao.schedule.get_database", new_callable=AsyncMock)
async def test_get_schedule(mock_get_database):
    mock_conn = mock_get_database.return_value
    mock_conn.fetchrow.return_value = {
        "id": 1,
        "customer_id": 1,
        "username": "user1",
        "service": "Cabelo",
        "start_time": datetime(2023, 1, 1, 10, 0)
    }

    result = await ScheduleDAO.get(1)

    assert result.id == 1
    assert result.customer_id == 1
    assert result.username == "user1"
    assert result.service == "Cabelo"
    assert result.start_time == datetime(2023, 1, 1, 10, 0)

@pytest.mark.asyncio
@patch("dao.schedule.get_database", new_callable=AsyncMock)
async def test_get_all_schedules(mock_get_database):
    # Arrange
    mock_conn = mock_get_database.return_value
    mock_conn.fetch.return_value = [
        {
            "id": 1,
            "customer_id": 1,
            "username": "user1",
            "service": "Cabelo",
            "start_time": datetime(2023, 1, 1, 10, 0)
        },
        {
            "id": 2,
            "customer_id": 2,
            "username": "user2",
            "service": "Barba",
            "start_time": datetime(2023, 1, 2, 10, 0)
        }
    ]

    result = await ScheduleDAO.get_all()

    assert len(result) == 2
    assert result[0].id == 1
    assert result[0].service == "Cabelo"
    assert result[1].id == 2
    assert result[1].service == "Barba"
