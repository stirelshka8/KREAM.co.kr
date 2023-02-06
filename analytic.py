import xlrd
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

rb = xlrd.open_workbook(f"{config['CONFIG']['save']}.xlsx")

sheet = rb.sheet_by_index(0)

for i in range(1, sheet.nrows):
    for j in range(0, sheet.ncols):
        print(sheet.cell_value(i, j), end='\t')
    print('')
