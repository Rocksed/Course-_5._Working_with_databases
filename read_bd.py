import psycopg2


class DBManager:
    def __init__(self, host, database, user, password):
        self.conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )

    def __del__(self):
        self.conn.close()

    def get_companies_and_vacancies_count(self):
        # Выполняет SQL-запрос, возвращающий имена компаний и количество вакансий, которые у них есть
        cur = self.conn.cursor()
        cur.execute("""
            SELECT e.name, COUNT(v.id) AS vacancies_count
            FROM employers e
            LEFT JOIN vacancies v ON e.id = v.employer_id
            GROUP BY e.id
        """)
        result = cur.fetchall()
        cur.close()
        return result

    def get_all_vacancies(self):
        # Выполняет SQL-запрос, возвращающий все вакансии, включая имена компаний, зарплаты, валюты и URL
        cur = self.conn.cursor()
        cur.execute("""
            SELECT e.name, v.name, v.salary_from, v.salary_to, v.salary_currency, v.url
            FROM employers e
            JOIN vacancies v ON e.id = v.employer_id
        """)
        result = cur.fetchall()
        cur.close()
        return result

    def get_avg_salary(self):
        # Выполняет SQL-запрос, возвращающий среднюю зарплату (salary_from и salary_to) для всех вакансий с валютой 'RUR'
        cur = self.conn.cursor()
        cur.execute("""
            SELECT AVG(salary_from), AVG(salary_to)
            FROM vacancies
            WHERE salary_currency = 'RUR'
        """)
        result = cur.fetchone()
        cur.close()
        return result

    def get_vacancies_with_higher_salary(self):
        # Выполняет SQL-запрос, возвращающий все вакансии с зарплатой выше, чем средняя зарплата для всех вакансий с валютой 'RUR
        cur = self.conn.cursor()
        cur.execute("""
            SELECT e.name, v.name, v.salary_from, v.salary_to, v.salary_currency, v.url
            FROM employers e
            JOIN vacancies v ON e.id = v.employer_id
            WHERE (v.salary_from + v.salary_to) / 2 > (
                SELECT AVG(salary_from + salary_to)
                FROM vacancies
                WHERE salary_currency = 'RUR'
            )
        """)
        result = cur.fetchall()
        cur.close()
        return result

    def get_vacancies_with_keyword(self, *keywords):
        # Выполняет SQL-запрос, возвращающий все вакансии, содержащие заданные ключевые слова в имени вакансии, используя полнотекстовый поиск
        keyword_str = ' | '.join(keywords)
        cur = self.conn.cursor()
        cur.execute(f"""
            SELECT e.name, v.name, v.salary_from, v.salary_to, v.salary_currency, v.url
            FROM employers e
            JOIN vacancies v ON e.id = v.employer_id
            WHERE to_tsvector('russian', v.name) @@ to_tsquery('russian', '{keyword_str}')
        """)
        result = cur.fetchall()
        cur.close()
        return result
