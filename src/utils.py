"""Вспомогательные функции для загрузки данных в БД."""

import psycopg2
from src.api_client import HHAPIClient

def save_employer_to_db(cur, employer_data: dict) -> None:
    """Сохраняет данные работодателя в таблицу employers."""
    cur.execute("""
        INSERT INTO employers (employer_id, company_name, site_url, description)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (employer_id) DO NOTHING;
    """, (
        employer_data['id'],
        employer_data.get('name'),
        employer_data.get('site_url'),
        employer_data.get('description')
    ))

def save_vacancies_to_db(cur, employer_id: int, vacancies: list) -> None:
    """Сохраняет список вакансий работодателя в таблицу vacancies."""
    for vac in vacancies:
        salary = vac.get('salary')
        salary_from = salary.get('from') if salary else None
        salary_to = salary.get('to') if salary else None
        currency = salary.get('currency') if salary else None
        cur.execute("""
            INSERT INTO vacancies (vacancy_id, employer_id, title, salary_from, salary_to, currency, url, requirement, responsibility)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (vacancy_id) DO NOTHING;
        """, (
            vac.get('id'), employer_id, vac.get('name'),
            salary_from, salary_to, currency,
            vac.get('alternate_url'),
            vac.get('snippet', {}).get('requirement'),
            vac.get('snippet', {}).get('responsibility')
        ))

def load_all_data(db_creator, employers_ids: list) -> None:
    """Основная функция загрузки данных обо всех работодателях и вакансиях."""
    client = HHAPIClient()
    conn = psycopg2.connect(
        dbname=db_creator.db_name,
        user=db_creator.user,
        password=db_creator.password,
        host=db_creator.host,
        port=db_creator.port
    )
    cur = conn.cursor()
    for emp_id in employers_ids:
        employer = client.get_employer(emp_id)
        save_employer_to_db(cur, employer)
        vacancies = client.get_vacancies_by_employer(emp_id)
        save_vacancies_to_db(cur, emp_id, vacancies)
    conn.commit()
    cur.close()
    conn.close()
