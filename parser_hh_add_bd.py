import psycopg2
import requests


class HHVacanciesLoader:
    def __init__(self, host, database, user, password):
        # Создаем объект для запросов к API HH
        self.url = 'https://api.hh.ru/vacancies'
        self.params = {
            'per_page': 100,
            'only_with_salary': True,
        }
        # Создаем подключение к базе данных PostgreSQL
        self.conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )

    def load_vacancies(self):
        # Получаем список вакансий с API HH
        response = requests.get(self.url, params=self.params)
        vacancies = response.json()['items']

        # Создаем курсор для выполнения SQL-запросов
        cur = self.conn.cursor()
        # Обрабатываем каждую вакансию из списка

        for vacancy in vacancies:
            employer = vacancy['employer']
            site_url = employer.get('site_url')
            logo_url = employer['logo_urls'].get('240') if employer.get('logo_urls') else None

            # Вставляем данные о работодателе в таблицу employers и получаем его id
            cur.execute(
                """
                INSERT INTO employers (name, site_url, logo_url)
                VALUES (%s, %s, %s)
                RETURNING id
                """,
                (employer['name'], site_url, logo_url),
            )
            employer_id = cur.fetchone()[0]

            # Получаем данные о зарплате и вставляем данные о вакансии в таблицу vacancies
            salary = vacancy['salary']
            cur.execute(
                """
                INSERT INTO vacancies (name, employer_id, salary_from, salary_to, salary_currency, published_at, url)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (vacancy['name'], employer_id, salary.get('from'), salary.get('to'), salary.get('currency'),
                 vacancy['published_at'], vacancy['alternate_url'])
            )

        # Сохраняем изменения в базе данных
        self.conn.commit()

        # Закрываем курсор
        cur.close()

    def close(self):
        # Закрываем соединение с базой данных
        self.conn.close()
