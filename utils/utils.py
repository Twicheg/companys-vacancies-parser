import psycopg2
import requests


def create_db(database_name: str, *, params: dict) -> None:
    """Функция создания database в postgresSQL
    create_db(database_name {str}, keyword params= {dict})"""
    con = psycopg2.connect(dbname='postgres', **params)
    con.autocommit = True
    cur = con.cursor()

    cur.execute("DROP DATABASE %s" % database_name)
    cur.execute("CREATE DATABASE %s" % database_name)

    cur.close()
    con.close()


def create_tables(table_names: list[str], db_name: str, *, params: dict) -> None:
    """Функция создания двух таблиц
    create_tables(table_names: [list[str]], database_name [str] , keyword params = [dict] """
    try:
        with psycopg2.connect(dbname=db_name, **params) as con:
            with con.cursor() as cur:
                cur.execute("DROP TABLE IF EXISTS %s CASCADE;" % table_names[0].lower())
                cur.execute("CREATE TABLE IF NOT EXISTS %s ("
                            "number serial,"
                            "company_id int primary key,"
                            "company_name varchar(255),"
                            "site varchar(255),"
                            "description text"
                            ")" % table_names[0].lower())
                cur.execute("DROP TABLE IF EXISTS %s CASCADE;" % table_names[1].lower())
                cur.execute("CREATE TABLE IF NOT EXISTS %s ("
                            "number serial ,"
                            "vacation_id int primary key,"
                            "company_id int references %s(company_id) not null,"
                            "vacation_name varchar(255),"
                            "salary_from int,"
                            "salary_to int,"
                            "salary_currency char(4),"
                            "vacation_url varchar(255),"
                            "requirement text,"
                            "responsibility text"
                            ")" % (table_names[1].lower(), table_names[0].lower()))

    except Exception as e:
        cur.close()
        con.close()
        print('Error: ', e)
    finally:
        con.close()


def fill_tables(table_names: list[str], db_name: str, *, company_ids: list[str], params: dict) -> None:
    """Функция заполнения таблиц с использованием API hh.ru
    fill_tables([tables_name:str],data_base_name:str,
    keyword compane_ids=[list[str]], keyword params=[dict])"""
    try:
        with psycopg2.connect(dbname=db_name, **params) as con:
            with con.cursor() as cur:
                for vacancy_id in company_ids:
                    response = requests.get(f"https://api.hh.ru/employers/{vacancy_id}")
                    site = response.json().get('site_url')
                    description = response.json().get('description', '')
                    for i in ('<p>', '<strong>', '</strong>', '</p>', '\xa0', '<ul>', '<li>', '</li>', '</ul>'):
                        if description is not None:
                            description = description.replace(i, '')
                        else:
                            description = 'null'

                    cur.execute("insert into %s (company_id,company_name,site,description)"
                                "values (%i,'%s','%s','%s')" %
                                (table_names[0].lower(),
                                 int(response.json().get('id')),
                                 response.json().get('name'),
                                 site,
                                 description))
                    for page in range(10):
                        for dict_ in requests.get(f"https://api.hh.ru/vacancies?employer_id={vacancy_id}",
                                                  params={'page': page, 'per_page': 100}).json()['items']:
                            if dict_.get('salary') is not None:
                                cur.execute("insert into %s (vacation_id,company_id,vacation_name,salary_from,"
                                            "salary_to,salary_currency,vacation_url,requirement,responsibility)"
                                            "values (%i,%i,'%s',%s,%s,'%s','%s','%s','%s')" % (
                                                table_names[1].lower(),
                                                int(dict_.get('id')),
                                                int(dict_['employer'].get('id')),
                                                dict_['name'],
                                                dict_['salary'].get('from') if dict_['salary'].get(
                                                    'from') is not None else 'null',
                                                dict_['salary'].get('to') if dict_['salary'].get(
                                                    'to') is not None else 'null',
                                                dict_['salary'].get('currency'),
                                                dict_['alternate_url'],
                                                dict_['snippet'].get('requirement'),
                                                dict_['snippet'].get('responsibility')))
                            else:
                                cur.execute("insert into %s (vacation_id,company_id,vacation_name,salary_from,"
                                            "salary_to,salary_currency,vacation_url,requirement,responsibility)"
                                            "values (%i,%i,'%s',%s,%s,'%s','%s','%s','%s')" % (
                                                table_names[1].lower(),
                                                int(dict_.get('id')),
                                                int(dict_['employer'].get('id')),
                                                dict_['name'],
                                                'null',
                                                'null',
                                                'null',
                                                dict_['alternate_url'],
                                                dict_['snippet'].get('requirement'),
                                                dict_['snippet'].get('responsibility')))

    except Exception as e:
        cur.close()
        con.close()
        print('Error: ', e)
    finally:
        con.close()
