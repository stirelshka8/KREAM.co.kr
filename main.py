import configparser
import os.path

print("""
██████╗░░█████╗░██████╗░░██████╗██╗███╗░░██╗░██████╗░
██╔══██╗██╔══██╗██╔══██╗██╔════╝██║████╗░██║██╔════╝░
██████╔╝███████║██████╔╝╚█████╗░██║██╔██╗██║██║░░██╗░
██╔═══╝░██╔══██║██╔══██╗░╚═══██╗██║██║╚████║██║░░╚██╗
██║░░░░░██║░░██║██║░░██║██████╔╝██║██║░╚███║╚██████╔╝
╚═╝░░░░░╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░╚═╝╚═╝░░╚══╝░╚═════╝░\n""")

if os.path.exists("config.ini"):
    import save_sheet
    import analytic

    config = configparser.ConfigParser()
    config.read("config.ini")

    if config['RUN']['extract_price'] == "True":
        set_metod = "извлечение данных СО стоимостью доставки"
    else:
        set_metod = "извлечение данных БЕЗ стоимости доставки"

    print(f"""Параметр сбора данных:
     1 - извлечение данных БЕЗ стоимости доставки;
     2 - извлечение данных СО стоимостью доставки (ВНИМАНИЕ!!! ВРЕМЯ ОБРАБОТКИ СИЛЬНО УВЕЛИЧИВАЕТСЯ);
     
     [INFO] После установки параметров необходимо заново запустить программу.
     
     [INFO] Ранее установленныq параметр - "{set_metod}."
     
Режим работы:
     3 - запуск процесса сбора данных;
     4 - запуск процесса анализа данных.\n\n""")
    mode = input("Выбранный режим > ")
    if mode == "1":
        config.set("RUN", "extract_price", "False")
        with open("config.ini", "w") as config_file:
            config.write(config_file)
    elif mode == "2":
        config.set("RUN", "extract_price", "True")
        with open("config.ini", "w") as config_file:
            config.write(config_file)
    elif mode == "3":
        save_sheet.save()
    elif mode == "4":
        analytic.save_analytic()
    else:
        print("Что то пошло не так!")



else:
    config = configparser.ConfigParser()
    config.read("config.ini")
    print("ПЕРВОНАЧАЛЬНАЯ НАСТРОЙКА\n\n")
    enter_search = input("Что будем парсить (например - lego)> ")
    enter_save = input("Имя файла куда будем сохранять извлеченные данные> ")
    enter_save_analytics = input("Имя файла куда будем сохранять данные аналитики > ")
    enter_save_brickset_login = input("Имя пользователя сайта https://brickset.com > ")
    enter_save_brickset_password = input("Пароль пользователя сайта https://brickset.com > ")
    print("-" * 50)
    print("""API токен необходимо получить на странице https://brickset.com/tools/webservices/requestkey, токен
        придет в ответном письме на почту.""")
    enter_save_brickset_api = input("API токен пользователя сайта https://brickset.com > ")
    print("-" * 50)
    print("""Адрес PROXY сервера брать отсюда http://free-proxy.cz/ru/proxylist/country/all/https/ping/all""")
    enter_save_proxy_addr = input("Адрес PROXY сервера (IP_АДРЕС:ПОРТ)> ")
    print("-" * 50)

    config.add_section("CONFIG")
    config.set("CONFIG", "search", enter_search)
    config.set("CONFIG", "save", enter_save)
    config.set("CONFIG", "save_analytics", enter_save_analytics)
    config.set("CONFIG", "brickset_login", enter_save_brickset_login)
    config.set("CONFIG", "brickset_password", enter_save_brickset_password)
    config.set("CONFIG", "brickset_api", enter_save_brickset_api)
    config.set("CONFIG", "proxy_metod", "https")
    config.set("CONFIG", "proxy_addr", enter_save_proxy_addr)

    config.add_section("INSTALL")
    config.set("INSTALL", "set_up", "True")
    config.set("INSTALL", "check_hash", "False")

    config.add_section("RUN")
    config.set("RUN", "extract_price", "False")

    with open("config.ini", "w") as config_file:
        config.write(config_file)
