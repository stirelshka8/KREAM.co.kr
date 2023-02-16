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

    response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies)
    print(response.text)
    return response.json()['sets'][0]['dimensions']


def __extract_price__(articular=None):
    if articular is not None:
        weight_start = round(__extract_size__(articular)['weight'], 1)

        if (weight_start % 1) < 0.5:
            converted_weight_start = float(f"{int(weight_start)}.5")
        elif (weight_start % 1) > 0.5:
            converted_weight_start = int(f"{int(weight_start) + 1}")
        else:
            converted_weight_start = int(weight_start)

        width = int(__extract_size__(articular)['width']) + 2
        length = int(__extract_size__(articular)['depth']) + 2
        height = int(__extract_size__(articular)['height']) + 2
        final_weight = 0
        temp_weight = round((width * length * height) / 6000, 1)

        if (temp_weight % 1) < 0.5:
            final_weight = float(f"{int(temp_weight)}.5")
        elif (temp_weight % 1) > 0.5:
            final_weight = int(f"{int(temp_weight) + 1}")

        if final_weight < converted_weight_start:
            final_weight = converted_weight_start

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
                  f"cal_weight={final_weight}&" \
                  f"weight={int(final_weight * 1000)}"

        response = requests.request("POST", url, data=payload)
        soup = BeautifulSoup(response.text, "html.parser")
        print(soup.find("div", class_="over_h m_b_40")) #!!!!!!!!!!!!!!!!!!!!! Доделать здесь
    else:
        print("Артикул товара не определен")


__extract_price__(76059)
