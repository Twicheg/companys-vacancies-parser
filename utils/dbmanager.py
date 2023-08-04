import psycopg2


class DBManager:
    def __init__(self, dbname, params):
        self.conn = psycopg2.connect(dbname=dbname, **params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        pass

    def get_all_vacancies(self):
        pass

    def get_avg_salary(self):
        pass

    def get_vacancies_with_higher_salary(self):
        pass

    def get_vacancies_with_keyword(self):
        pass
    def __getattr__(self, item):
        print(f'Метод {item}')

    def __del__(self):
        self.cur.close()
        self.conn.close()
        print('Деструктор')