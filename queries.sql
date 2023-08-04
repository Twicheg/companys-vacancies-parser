/* get_companies_and_vacancies_count

select company_name,count(vacations.vacation_id) from companies
join vacations using(company_id)
group by company_name;

/* get_all_vacancies

select companies.company_name,vacation_name,salary_from,salary_to,salary_currency,vacation_url
from vacations
join companies using(company_id);

/* get_avg_salary
select vacation_name, ROUND(avg(salary_to)) as salary_to , ROUND(avg(salary_from)) as salary_from
from vacations
group by vacation_name

/* get_avg_salary

select vacation_name from vacations join companies using(company_id)
where salary_to > (select avg(salary_to)/count(*) from vacations)
and salary_from > (select avg(salary_from)/count(*) from vacations)

/* get_vacancies_with_keyword

select vacation_name from vacations
where vacation_name like '%python%'
or vacation_name like '%python'
or vacation_name like 'python%';