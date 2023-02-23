import configparser
import os.path

print("""

██████╗░░█████╗░██████╗░░██████╗██╗███╗░░██╗░██████╗░  ██╗░░██╗██████╗░███████╗░█████╗░███╗░░░███╗
██╔══██╗██╔══██╗██╔══██╗██╔════╝██║████╗░██║██╔════╝░  ██║░██╔╝██╔══██╗██╔════╝██╔══██╗████╗░████║
██████╔╝███████║██████╔╝╚█████╗░██║██╔██╗██║██║░░██╗░  █████═╝░██████╔╝█████╗░░███████║██╔████╔██║
██╔═══╝░██╔══██║██╔══██╗░╚═══██╗██║██║╚████║██║░░╚██╗  ██╔═██╗░██╔══██╗██╔══╝░░██╔══██║██║╚██╔╝██║
██║░░░░░██║░░██║██║░░██║██████╔╝██║██║░╚███║╚██████╔╝  ██║░╚██╗██║░░██║███████╗██║░░██║██║░╚═╝░██║
╚═╝░░░░░╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░╚═╝╚═╝░░╚══╝░╚═════╝░  ╚═╝░░╚═╝╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝╚═╝░░░░░╚═╝ for Andrey \n""")

if os.path.exists("config.ini"):
    import save_sheet
    import analytic

    config = configparser.ConfigParser()
    config.read("config.ini")

    print(f"""     
Режим работы:
     3 - запуск процесса сбора данных;
     4 - запуск процесса анализа данных.\n\n""")
    mode = input("Выбранный режим > ")
    if mode == "3":
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

    config.add_section("CONFIG")
    config.set("CONFIG", "search", enter_search)
    config.set("CONFIG", "save", enter_save)
    config.set("CONFIG", "save_analytics", enter_save_analytics)

    config.add_section("INSTALL")
    config.set("INSTALL", "set_up", "True")

    with open("config.ini", "w") as config_file:
        config.write(config_file)
