import xlrd
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
read_book = xlrd.open_workbook(f"{config['CONFIG']['save']}.xlsx")
SHEET_NAME = f"{config['CONFIG']['save_analytics']}"
read_sheet_one = read_book.sheet_by_index(0)
read_sheet_two = read_book.sheet_by_index(1)


def search_one():
    comparison = []
    for iter_line in (range(1, max(read_sheet_one.nrows, read_sheet_two.nrows))):
        for iter_column in range(0, 6):
            comparison_temp = []
            try:
                if read_sheet_one.cell_value(iter_line, iter_column) != read_sheet_two.cell_value(iter_line, iter_column):
                    comparison_temp.append(read_sheet_one.cell_value(iter_line, iter_column))
            except IndexError:
                pass
            comparison.append(comparison_temp)
    print(comparison)


if __name__ == "__main__":
    search_one()
