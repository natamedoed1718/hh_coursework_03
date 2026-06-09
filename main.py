from src.utils import load_all_data
from src.db_creator import DBCreator
from src.db_manager import DBManager

EMPLOYERS = [1455, 78638, 3776, 80, 3529, 2180, 15478, 1057, 39305, 2381]


def user_interaction():
    db = DBManager()
    while True:
        print("\n" + "=" * 50)
        print("Управление вакансиями".center(50))
        print("=" * 50)
        print("1. Список компаний и количество вакансий")
        print("2. Список всех вакансий")
        print("3. Средняя зарплата по вакансиям")
        print("4. Вакансии с зарплатой выше средней")
        print("5. Поиск вакансий по ключевому слову")
        print("0. Выход")
        choice = input("\nВыберите действие (0-5): ")

        if choice == "1":
            result = db.get_companies_and_vacancies_count()
            if not result:
                print("Нет данных.")
            for company_name, vacancies_count in result:
                print(f"Компания: {company_name} | Вакансий: {vacancies_count}")

        elif choice == "2":
            result = db.get_all_vacancies()
            if not result:
                print("Нет вакансий.")
            for company_name, title, salary, url in result:
                salary_str = f"{int(salary)}" if salary else "не указана"
                print(
                    f"Компания: {company_name}\nВакансия: {title}\nЗарплата: {salary_str}\nСсылка: {url}\n"
                )

        elif choice == "3":
            avg = db.get_avg_salary()
            print(f"Средняя зарплата по всем вакансиям: {avg:.2f}")

        elif choice == "4":
            result = db.get_vacancies_with_higher_salary()
            if not result:
                print("Нет вакансий с зарплатой выше средней.")
            for company_name, title, salary, url in result:
                print(
                    f"Компания: {company_name} | {title} | Зарплата: {salary} | {url}"
                )

        elif choice == "5":
            keyword = input("Введите ключевое слово (например, 'python'): ")
            result = db.get_vacancies_with_keyword(keyword)
            if not result:
                print(f"Вакансии с '{keyword}' не найдены.")
            for company_name, title, url in result:
                print(f"Компания: {company_name}\nВакансия: {title}\nСсылка: {url}\n")

        elif choice == "0":
            print("Выход.")
            break
        else:
            print("Неверный ввод. Попробуйте снова.")


if __name__ == "__main__":
    creator = DBCreator()
    creator.create_database()
    creator.create_tables()
    load_all_data(creator, EMPLOYERS)
    user_interaction()
