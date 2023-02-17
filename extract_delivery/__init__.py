import requests
import configparser
from bs4 import BeautifulSoup

config = configparser.ConfigParser()
config.read("../config.ini")


def __extract_size__(articular):
    proxies = {f"{config['CONFIG']['proxy_metod']}": f"{config['CONFIG']['proxy_addr']}"}
    url = "https://brickset.com/api/v3.asmx/getSets"
    queryty = {'query': f"{articular}"}

    payload = f"apiKey={config['CONFIG']['brickset_api']}&userHash={config['CONFIG']['brickset_hash']}&params={queryty}"
    headers = {
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        'Host': "brickset.com",
        'Referer': "https://brickset.com/",
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0",
        'Content-Type': "application/x-www-form-urlencoded"
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies)
        return response.json()['sets'][0]['dimensions']
    except requests.exceptions.ProxyError:
        print("Ошибка PROXY!!!!")


def __extract_price__(articular=None):
    artic_list = []
    if articular is not None:
        artic_list.append(__extract_size__(articular))
        converted_final_weight = 0
        weight_start = round(artic_list[0]['weight'], 1)
        if (weight_start % 1) < 0.5:
            converted_weight_start = float(f"{int(weight_start)}.5")
        elif (weight_start % 1) > 0.5:
            converted_weight_start = int(f"{int(weight_start) + 1}")
        else:
            converted_weight_start = int(weight_start)

        width = int(artic_list[0]['width']) + 2
        length = int(artic_list[0]['depth']) + 2
        height = int(artic_list[0]['height']) + 2
        temp_weight = round((width * length * height) / 6000, 1)

        if (temp_weight % 1) < 0.5:
            converted_final_weight = float(f"{int(temp_weight)}.5")
        elif (temp_weight % 1) > 0.5:
            converted_final_weight = int(f"{int(temp_weight)}")

        if converted_final_weight < converted_weight_start:
            converted_final_weight = converted_weight_start

        url = "https://ems.epost.go.kr/front.EmsDeliveryDelivery09.postal"
        payload = f"cmd=compute&" \
                  f"owlh=0.0&" \
                  f"nwlh=0.0&" \
                  f"recprcapplyareacd=RU&" \
                  f"reclimitwght=30000&" \
                  f"langtype=en&" \
                  f"emsgubun=01&" \
                  f"paper=N&" \
                  f"insurYn=N&" \
                  f"insrAmount=0&" \
                  f"frnTranspPartyDivCd=1&" \
                  f"nation=RU&" \
                  f"realWght={converted_weight_start}&" \
                  f"vwidth={width}&" \
                  f"vlength={length}&" \
                  f"vheight={height}&" \
                  f"cal_weight={converted_final_weight}&" \
                  f"weight={int(converted_final_weight * 1000)}"

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'ems.epost.go.kr',
            'Origin': 'https://ems.epost.go.kr',
            'Referer': 'https://ems.epost.go.kr/front.EmsDeliveryDelivery09.postal',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0',
            'Cookie': 'JSESSIONID=QqCJ3Pmy30Ix1S0aiBu41nQChv2jZHncCcYyO8OZbk0Chi8MbXYUO5zHiUF1GWjO.epost3_servlet_parcel; clientid=070081942957'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        soup = BeautifulSoup(response.text, "html.parser")
        exit_data = (soup.find(class_="table_row v2").findAll(class_="blue2")[1]).text
        format_data_price = exit_data.split(" ")
        return format_data_price[0]
    else:
        print("Артикул товара не определен")


print(__extract_price__(76059))
