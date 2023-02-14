import requests
import configparser

config = configparser.ConfigParser()
config.read("config.ini")


def __extract_size__(que):
    url = "https://brickset.com/api/v3.asmx/getSets"
    queryty = {'query': f"{que}"}

    payload = f"apiKey={config['CONFIG']['brickset_api']}&userHash={config['CONFIG']['brickset_hash']}&params={queryty}"
    headers = {
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        'Accept-Encoding': "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        'Cookie': f"{config['CONFIG']['cookie']}",
        'Host': "brickset.com",
        'Referer': "https://brickset.com/",
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0",
        'Content-Type': "application/x-www-form-urlencoded"
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()['sets'][0]['dimensions']

if __name__:
    print(__name__)
