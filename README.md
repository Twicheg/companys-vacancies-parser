# Курсовая работа №5

### создана функция main() модуля main.py

для получения,сохранения и обработки данных , полученных с API hh.ru 

принимает список id компаний с сайта hh.ru, \
названия ДБ для создания в postgresSQL , \
список названия таблиц

### создан файл database.ini с параметрами подключения к БД
пример содержания файла database.ini: \
`[postgresql]`\
`host=localhost` \
`user=postgres` \
`password=****`\
`port=5432`

### из utils.py импортировано 3 функции:
* `create_db` для создания ДБ
* `create_tables` для создания таблиц в ДБ
* `fill_tables` для подключения к API.hh.ru и заполнения таблиц данными

### из config.py импортирована функция:
* `config ` для извлечения из database.ini параметров для подключения к БД


### создан и импортирован класса DBManager ,который будет подключаться к БД Postgres и имеет следующие методы:

- `get_companies_and_vacancies_count()`: получает список всех компаний и количество вакансий у каждой компании.
- `get_all_vacancies()`: получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
- `get_avg_salary()`: получает среднюю зарплату по вакансиям.
- `get_vacancies_with_higher_salary()`: получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
- `get_vacancies_with_keyword()`: получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”.

код функции main: \
`def main(companies_ids: list[str], db_name: str, tables_names: list[str]) -> None:`\
    `create_db(db_name, params=config())` \
    `create_tables(tables_names, db_name.lower(), params=config())` \
    `fill_tables(tables_names, db_name.lower(), company_ids=companies_ids, params=config())` \
    `db = DBManager(db_name.lower(), config())` \
    `db.get_companies_and_vacancies_count()` \
    `db.get_all_vacancies()` \
    `db.get_avg_salary()` \
    `db.get_vacancies_with_higher_salary()` \
    `db.get_vacancies_with_keyword()` \
    `del db`
