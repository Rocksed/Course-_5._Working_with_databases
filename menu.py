import sys
from read_bd import DBManager
from parser_hh_add_bd import HHVacanciesLoader

bd_host = input('Введите host: ')
bd_database = input('Введите название базы данных: ')
bd_user = input('Введите пользователя базы данных: ')
bd_password = input('Введите пароль базы данных: ')
loader = HHVacanciesLoader(host=bd_host, database=bd_database, user=bd_user, password=bd_password)
loader.load_vacancies()
loader.close()
db = DBManager(host=bd_host, database=bd_database, user=bd_user, password=bd_password)

while True:
    print("Выберите действие:")
    print("1. Получить список всех компаний и количество вакансий у каждой компании")
    print(
        "2. Получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию")
    print("3. Получить среднюю зарплату по вакансиям")
    print("4. Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям")
    print("5. Получить список всех вакансий, в названии которых содержатся переданные в метод слова")
    print("0. Выйти")

    choice = input("Выберите действие (цифру): ")

    if choice == "0":
        sys.exit(0)

    elif choice == "1":
        companies_and_vacancies = db.get_companies_and_vacancies_count()
        print(companies_and_vacancies)

    elif choice == "2":
        all_vacancies = db.get_all_vacancies()
        print(all_vacancies)

    elif choice == "3":
        avg_salary = db.get_avg_salary()
        print(f"Средняя зарплата по вакансиям: {avg_salary}")

    elif choice == "4":
        vacancies_with_higher_salary = db.get_vacancies_with_higher_salary()
        print(vacancies_with_higher_salary)

    elif choice == "5":
        keyword = input("Введите ключевое слово: ")
        vacancies_with_keyword = db.get_vacancies_with_keyword(keyword)
        print(vacancies_with_keyword)

    else:
        print("Некорректный выбор")
