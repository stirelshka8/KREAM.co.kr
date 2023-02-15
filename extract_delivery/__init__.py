import requests
import configparser

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
    return response.json()['sets'][0]['dimensions']


def __extract_price__(articular=None):
    if articular is not None:
        weight = 20
        width = 59
        length = 50
        height = 19
        final_weight = (width * length * height) / 6000

        if final_weight < weight:
            final_weight = weight

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
                  f"realWght={weight}&" \
                  f"vwidth={width}&" \
                  f"vlength={length}&" \
                  f"vheight={height}&" \
                  f"cal_weight={final_weight}&" \
                  f"weight={final_weight * 1000}"

        print(payload)

        # response = requests.request("POST", url, data=payload)
        # print(response.text)
    else:
        print("Артикул товара не определен")



