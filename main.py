import configparser
import save_sheet
import analytic

config = configparser.ConfigParser()
config.read("config.ini")

save_sheet.save()
analytic.save_analytic()
