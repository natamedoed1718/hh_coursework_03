import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

load_dotenv()

class DBCreator:
    """Создание базы данных и таблиц."""

    def __init__(self):
        self.db_name = os.getenv("DB_NAME")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")

    def create_database(self) -> None:
        """Создаёт БД, если она не существует."""
        conn = psycopg2.connect(dbname="postgres", user=self.user,
                                password=self.password, host=self.host, port=self.port)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname='{self.db_name}'")
        if not cur.fetchone():
            cur.execute(f"CREATE DATABASE {self.db_name}")
        cur.close()
        conn.close()

    def create_tables(self) -> None:
        """Создаёт таблицы employers и vacancies."""
        with psycopg2.connect(dbname=self.db_name, user=self.user,
                              password=self.password, host=self.host, port=self.port) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS employers (
                        employer_id INT PRIMARY KEY,
                        company_name VARCHAR(255) NOT NULL,
                        site_url TEXT,
                        description TEXT
                    );
                """)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS vacancies (
                        vacancy_id INT PRIMARY KEY,
                        employer_id INT REFERENCES employers(employer_id),
                        title VARCHAR(255) NOT NULL,
                        salary_from INT,
                        salary_to INT,
                        currency VARCHAR(3),
                        url TEXT,
                        requirement TEXT,
                        responsibility TEXT
                    );
                """)
            conn.commit()

