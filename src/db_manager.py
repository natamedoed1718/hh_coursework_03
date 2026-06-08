import psycopg2
from typing import List, Tuple, Any
import os
from dotenv import load_dotenv

load_dotenv()

class DBManager:
    """Класс для работы с БД (методы по ТЗ)."""

    def __init__(self):
        self.db_name = os.getenv("DB_NAME")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")

    def _get_connection(self):
        return psycopg2.connect(dbname=self.db_name, user=self.user,
                                password=self.password, host=self.host, port=self.port)

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """Список компаний и количество вакансий у каждой."""
        query = """
            SELECT e.company_name, COUNT(v.vacancy_id)
            FROM employers e
            LEFT JOIN vacancies v ON e.employer_id = v.employer_id
            GROUP BY e.employer_id
            ORDER BY e.company_name;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return cur.fetchall()

    def get_all_vacancies(self) -> List[Tuple[str, str, Any, str]]:
        """Список вакансий: компания, название, зарплата, ссылка."""
        query = """
            SELECT e.company_name, v.title,
                   COALESCE(v.salary_from, v.salary_to, 0) as salary_display,
                   v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return cur.fetchall()

    def get_avg_salary(self) -> float:
        """Средняя зарплата по вакансиям (берём salary_from или salary_to)."""
        query = """
            SELECT AVG(COALESCE(salary_from, salary_to, 0))
            FROM vacancies
            WHERE salary_from IS NOT NULL OR salary_to IS NOT NULL;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchone()[0]
                return result if result else 0.0

    def get_vacancies_with_higher_salary(self) -> List[Tuple]:
        """Вакансии с зарплатой выше средней."""
        avg = self.get_avg_salary()
        query = """
            SELECT e.company_name, v.title,
                   COALESCE(v.salary_from, v.salary_to, 0) as salary,
                   v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id
            WHERE COALESCE(v.salary_from, v.salary_to, 0) > %s;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (avg,))
                return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple]:
        """Вакансии, в названии которых есть keyword."""
        query = """
            SELECT e.company_name, v.title, v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id
            WHERE v.title ILIKE %s;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (f"%{keyword}%",))
                return cur.fetchall()
