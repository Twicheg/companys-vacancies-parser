import requests,time

def get_vacation_list() -> list:
    URL = 'https://api.hh.ru/vacancies'
    vacations_list = []
    page = 0

    while True:
        time.sleep(0.5)
        params = {
                'page': page,
                'per_page': 100
            }
        header = {'User-Agent': 'MyApp'}
        response = requests.get(URL, params=params,headers=header)
        if not response.ok:
            break
        vacations_list.extend(response.json()['items'])
        page += 1
        # if page == 1 :
        #     print(vacations_list,file=open('test.json','w'))
    # employers_id = '1740'
    # URL1 = f'https://api.hh.ru/employers/{employers_id}'
    # response = requests.get(URL1)
    # print(response.json(), file=open('test1.json', 'w'))
    return vacations_list
