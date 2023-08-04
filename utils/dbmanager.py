import psycopg2


class DBManager:
    """Класс работы с базой данных
    __init__(self, dbname[str], params[dict])"""

    def __init__(self, dbname: str, params: dict) -> None:
        self.conn = psycopg2.connect(dbname=dbname, **params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self) -> list[tuple]:
        """Метод обращения к ДБ ,
         get_companies_and_vacancies_count(self)
         return [list[tuple]] tuple (компаний ,кол-во вакансий у компаний)"""
        self.cur.execute('select company_name,count(vacations.vacation_id) from companies '
                         'join vacations using(company_id)'
                         'group by company_name;')
        return self.cur.fetchall()

    def get_all_vacancies(self) -> list[tuple]:
        """Метод обращения к ДБ  ,
        get_all_vacancies(self) ,
        return [list[tuple]] tuple(список всех вакансий , названия компании,
        названия вакансии , зарплата , ссылка на вакансию)"""
        self.cur.execute(
            'select companies.company_name,vacation_name,salary_from,salary_to,salary_currency,vacation_url'
            ' from vacations '
            ' join companies using(company_id);')
        return self.cur.fetchall()

    def get_avg_salary(self) -> list[tuple]:
        """Метод возвращает среднюю зарплату по вакансиям
        get_avg_salary(self),
        return [list[tuple]] tuple:(вакансия,средняя зарплата)"""
        avg_list = []
        self.cur.execute(
            'select vacation_name, ROUND(avg(salary_to)) as salary_to , ROUND(avg(salary_from)) as salary_from '
            'from vacations '
            'group by vacation_name;')
        for v, st, sf in self.cur.fetchall():
            if st is None and sf is None:
                avg_list.append((v, 0))
            elif st is None and sf is not None:
                avg_list.append((v, sf))
            elif st is not None and sf is None:
                avg_list.append((v, st))
            elif st is not None and sf is not None:
                avg_list.append((v, int((sf + st) / 2)))
        return avg_list

    def get_vacancies_with_higher_salary(self) -> list:
        """Метод возвращает список ваканский с зарплатой выше средней
        get_vacancies_with_higher_salary(self)
        return [list] """
        list_vacancies_with_higher_salary = []
        self.cur.execute('select vacation_name from vacations join companies using(company_id) '
                         'where salary_to > (select avg(salary_to)/count(*) from vacations) '
                         'and salary_from > (select avg(salary_from)/count(*) from vacations)')
        for i in self.cur.fetchall():
            list_vacancies_with_higher_salary.append(i[0])
        return list_vacancies_with_higher_salary

    def get_vacancies_with_keyword(self, def_word='python') -> list:
        """ Метод возвращает список ваканский , искомые по ключевому слову
        get_vacancies_with_keyword(self, ключ.слово)
         return [list]"""
        list_vacancies_with_keyword = []
        self.cur.execute(f"select vacation_name from vacations "
                         f"where vacation_name like '%{def_word}%' "
                         f"or vacation_name like '%{def_word}' "
                         f"or vacation_name like '{def_word}%';")
        for i in self.cur.fetchall():
            list_vacancies_with_keyword.append(i[0])
        return list_vacancies_with_keyword

    def __del__(self):
        self.cur.close()
        self.conn.close()
