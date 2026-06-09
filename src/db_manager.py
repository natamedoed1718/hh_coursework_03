import os
import psycopg2
from typing import  List, Tuple, cast
from dotenv import load_dotenv
from psycopg2.extensions import connection

load_dotenv()


class DBManager:
    def __init__(self) -> None:
        self.db_name = os.getenv("DB_NAME")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")

    def _get_connection(self) -> connection:
        return psycopg2.connect(
            dbname=self.db_name,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        query = """
            SELECT e.company_name, COUNT(v.vacancy_id)
            FROM employers e
            LEFT JOIN vacancies v ON e.employer_id = v.employer_id
            GROUP BY e.employer_id
            ORDER BY e.company_name
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
                return cast(List[Tuple[str, int]], rows)

    def get_all_vacancies(self) -> List[Tuple[str, str, float, str]]:
        query = """
            SELECT e.company_name, v.title,
                   COALESCE(v.salary_from, v.salary_to, 0) as salary_display,
                   v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
                # Преобразуем salary к float, если нужно
                typed_rows: List[Tuple[str, str, float, str]] = []
                for row in rows:
                    typed_rows.append((row[0], row[1], float(row[2]), row[3]))
                return typed_rows

    def get_avg_salary(self) -> float:
        query = """
            SELECT AVG(COALESCE(salary_from, salary_to, 0))
            FROM vacancies
            WHERE salary_from IS NOT NULL OR salary_to IS NOT NULL
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchone()
                if result and result[0] is not None:
                    return float(result[0])
                return 0.0

    def get_vacancies_with_higher_salary(self) -> List[Tuple[str, str, float, str]]:
        avg = self.get_avg_salary()
        query = """
            SELECT e.company_name, v.title,
                   COALESCE(v.salary_from, v.salary_to, 0) as salary,
                   v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id
            WHERE COALESCE(v.salary_from, v.salary_to, 0) > %s
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (avg,))
                rows = cur.fetchall()
                return [(row[0], row[1], float(row[2]), row[3]) for row in rows]

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple[str, str, str]]:
        query = """
            SELECT e.company_name, v.title, v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id
            WHERE v.title ILIKE %s
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (f"%{keyword}%",))
                rows = cur.fetchall()
                return cast(List[Tuple[str, str, str]], rows)
