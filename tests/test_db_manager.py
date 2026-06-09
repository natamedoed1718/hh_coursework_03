import pytest
from src.db_manager import DBManager

def test_get_companies_and_vacancies_count(db_manager: DBManager):
    # Вставляем тестовые данные напрямую через курсор
    with db_manager._get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM vacancies")
            cur.execute("DELETE FROM employers")
            cur.execute("INSERT INTO employers (employer_id, company_name) VALUES (1, 'Test Company')")
            cur.execute("INSERT INTO vacancies (vacancy_id, employer_id, title) VALUES (100, 1, 'Test Vacancy')")
        conn.commit()

    result = db_manager.get_companies_and_vacancies_count()
    assert len(result) == 1
    assert result[0][0] == 'Test Company'
    assert result[0][1] == 1

def test_get_avg_salary(db_manager: DBManager):
    with db_manager._get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM vacancies")
            cur.execute("INSERT INTO vacancies (vacancy_id, employer_id, title, salary_from, salary_to) VALUES (1, 1, 'Job1', 1000, 2000)")
            cur.execute("INSERT INTO vacancies (vacancy_id, employer_id, title, salary_from, salary_to) VALUES (2, 1, 'Job2', 3000, 4000)")
        conn.commit()

    avg = db_manager.get_avg_salary()
    # Среднее от (1000+2000)/2? Нет, функция берёт
    # COALESCE(salary_from, salary_to, 0) => 1000 и 3000 -> среднее 2000
    assert avg == 2000.0

