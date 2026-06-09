import pytest
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv
from src.db_manager import DBManager

load_dotenv()

@pytest.fixture(scope="session")
def test_db():
    """Создаёт тестовую базу данных и возвращает параметры подключения."""
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    test_db_name = "hh_test"

    # Подключаемся к postgres, чтобы создать тестовую БД
    conn = psycopg2.connect(
        dbname="postgres",
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {test_db_name}")
    cur.execute(f"CREATE DATABASE {test_db_name}")
    cur.close()
    conn.close()

    # Создаём таблицы в тестовой БД (можно использовать DBCreator)
    from src.db_creator import DBCreator
    creator = DBCreator()
    creator.db_name = test_db_name
    creator.create_tables()  # нужно, чтобы метод create_tables использовал self.db_name

    yield {
        "db_name": test_db_name,
        "user": db_user,
        "password": db_password,
        "host": db_host,
        "port": db_port
    }

    # После тестов удаляем тестовую БД
    conn = psycopg2.connect(
        dbname="postgres",
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {test_db_name}")
    cur.close()
    conn.close()


@pytest.fixture
def db_manager(test_db):
    """Возвращает DBManager, настроенный на тестовую БД."""
    manager = DBManager()
    # Подменяем параметры подключения на тестовые
    manager.db_name = test_db["db_name"]
    manager.user = test_db["user"]
    manager.password = test_db["password"]
    manager.host = test_db["host"]
    manager.port = test_db["port"]
    return manager
