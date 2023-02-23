import requests
import configparser
from bs4 import BeautifulSoup

config = configparser.ConfigParser()
config.read("../config.ini")


def __extract_size__(articular):
    url = f"https://www.bricklink.com/v2/catalog/catalogitem.page?S={articular}"

    payload = {}
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0'}

    response = requests.request("GET", url, headers=headers, data=payload)
    soup = BeautifulSoup(response.text, "html.parser")
    exit_data_size = (soup.find(id="id_divBlock_Main").find(id="dimSec")).text
    exit_data_weight = (soup.find(id="id_divBlock_Main").find(id="item-weight-info")).text
    edited_output_size = exit_data_size.split(" ")
    edited_output_weight = exit_data_weight[0:-1]

    return [float(edited_output_size[0]),
            float(edited_output_size[2]),
            float(edited_output_size[4]),
            float(edited_output_weight)]


def __extract_price__(articular=None):
    artic_list = __extract_size__(articular)
    reformat_weight = round(artic_list[3] / 1000, 1)
    calibrate_weight = (int(artic_list[0] + 2) * (int(artic_list[1] + 2)) * (int(artic_list[2] + 2))) / 6000

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
              f"realWght={reformat_weight}&" \
              f"vwidth={int(artic_list[0] + 2)}&" \
              f"vlength={int(artic_list[1] + 2)}&" \
              f"vheight={int(artic_list[2] + 2)}&" \
              f"cal_weight={calibrate_weight}&" \
              f"weight={int(reformat_weight * 1000)}"

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'ems.epost.go.kr',
        'Origin': 'https://ems.epost.go.kr',
        'Referer': 'https://ems.epost.go.kr/front.EmsDeliveryDelivery09.postal',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0',
        'Cookie': 'JSESSIONID=QqCJ3Pmy30Ix1S0aiBu41nQChv2jZHncCcYyO8OZbk0Chi8MbXYUO5zHiUF1GWjO'
                  '.epost3_servlet_parcel; clientid=070081942957'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    soup = BeautifulSoup(response.text, "html.parser")
    exit_data = (soup.find(class_="table_row v2").findAll(class_="blue2")[1]).text
    format_data_price = exit_data.split(" ")
    print(payload)

    return format_data_price[0]
