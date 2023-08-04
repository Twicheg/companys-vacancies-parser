import psycopg2
from utils.api_hh import get_vacation_list
from utils.dbmanager import DBManager
from utils.utils import create_db, create_tables, fill_tables
from utils.config import config


def main(company_ids):
    db_name = 'MyDB'
    table_names = ['Companies', 'Vacations']
    #create_db(db_name, params=config())
    create_tables(table_names, db_name.lower(), params=config())
    fill_tables(table_names, db_name.lower(), company_ids=company_ids, params=config())
    db = DBManager(db_name.lower(), config())
    db.get_companies_and_vacancies_count()
    db.get_all_vacancies()
    db.get_avg_salary()
    db.get_vacancies_with_higher_salary()
    db.get_vacancies_with_keyword()
    del db


if __name__ == '__main__':
    company_ids = ['1740', '724229', '4156686', '1776381',
    '723204', '1579449', '2324020', '710', '1239730']
    main(company_ids)
