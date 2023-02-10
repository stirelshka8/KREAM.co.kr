import requests
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

search = config['CONFIG']['search']
temer = float(config['CONFIG']['timer'])

start_url = f"https://kream.co.kr/api/p/products?keyword={search}&per_page=50&cursor=1"

payload = {}
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0',
    'X-KREAM-API-VERSION': '14',
    'X-KREAM-CLIENT-DATETIME': '20230131211650+0300',
    'X-KREAM-DEVICE-ID': 'web;ceed1fd5-d4b1-48ce-aab8-dae9e6b85c04'
}

response = requests.request("GET", start_url, headers=headers, data=payload)

data_list = [response.json()["total"],
             response.json()["per_page"],
             (response.json()["total"]) // (response.json()["per_page"])]


def _extract_page():
    count_page = 1
    page_list = []
    while count_page < data_list[2] + 1:
        page_list.append(f'https://kream.co.kr/api/p/products?keyword={search}&per_page=50&cursor={count_page}')
        count_page += 1
    return page_list


def _extract_data():
    counter = 1
    export_list = []
    dict_size = {}

    for extractus in _extract_page():
        print(f'Обрабатывается {counter} страница из {data_list[2]}')
        payload_data = {}
        headers_data = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0',
            'X-KREAM-API-VERSION': '14',
            'X-KREAM-CLIENT-DATETIME': '20230131211650+0300',
            'X-KREAM-DEVICE-ID': 'web;ceed1fd5-d4b1-48ce-aab8-dae9e6b85c04'
        }
        response_data = requests.request("GET", extractus, headers=headers_data, data=payload_data)

        for item in response_data.json()['items']:
            # print(item)
            if item['market']['lowest_ask'] is not None:
                lowest = item['market']['lowest_ask']
            else:
                lowest = '0'

            if item['market']['last_sale_price'] is not None:
                last_sale = item['market']['last_sale_price']
            else:
                last_sale = '0'

            if item['release']['date_released'] is not None:
                date_rel = item['release']['date_released']
            else:
                date_rel = '0'

            import_list = [f"https://kream.co.kr/products/{item['release']['id']}", item['release']['name'],
                           item['release']['style_code'], lowest, last_sale, date_rel, item['counter']['wish_count']]

            export_list.append(import_list)

        counter += 1

    return export_list
