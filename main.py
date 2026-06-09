from src.db_creator import DBCreator
from src.db_manager import DBManager
from src.utils import load_all_data

EMPLOYERS = [1455, 78638, 3776, 80, 3529, 2180, 15478, 1057, 39305, 2381]


def user_interaction() -> None:
    db = DBManager()
    while True:
        choice = input("...")
        if choice == '1':
            companies = db.get_companies_and_vacancies_count()
            for name, cnt in companies:
                print(f"{name}: {cnt}")
        elif choice == '2':
            vacancies = db.get_all_vacancies()
            for company, title, salary, url in vacancies:
                print(f"{company} | {title} | {salary} | {url}")
        elif choice == '3':
            avg = db.get_avg_salary()
            print(f"Средняя зарплата: {avg:.2f}")
        elif choice == '4':
            high_salary = db.get_vacancies_with_higher_salary()
            for company, title, salary, url in high_salary:
                print(f"{company} | {title} | {salary} | {url}")
        elif choice == '5':
            keyword = input("Ключевое слово: ")
            keyword_vacancies = db.get_vacancies_with_keyword(keyword)
            for company, title, url in keyword_vacancies:
                print(f"{company} | {title} | {url}")


if __name__ == "__main__":
    creator = DBCreator()
    creator.create_database()
    creator.create_tables()
    load_all_data(creator, EMPLOYERS)
    user_interaction()
