import xlrd
import configparser
from save_sheet import save

config = configparser.ConfigParser()
config.read("config.ini")
read_book = xlrd.open_workbook(f"{config['CONFIG']['save']}.xlsx")
number_sheets = (len(read_book.sheet_names()) - 1)  # Единица вычитается, так как отсчет идет с 0
sheet_name = f"{config['CONFIG']['save_analytics']}"
read_sheet_penultimate = read_book.sheet_by_index(number_sheets - 1)
read_sheet_last = read_book.sheet_by_index(number_sheets)


def data_extraction():
    if len(read_book.sheet_names()) >= 1:
        penultimate_list = []
        last_list = []
        for iter_line in (range(1, max(read_sheet_penultimate.nrows, read_sheet_last.nrows))):
            penultimate_list_temp = []
            last_list_temp = []

            for iter_column in range(0, 7):
                if iter_line >= read_sheet_penultimate.nrows:
                    penultimate_list_temp.append(
                        read_sheet_penultimate.cell_value(read_sheet_penultimate.nrows, iter_column))
                else:
                    penultimate_list_temp.append(read_sheet_penultimate.cell_value(iter_line, iter_column))

                if iter_line >= read_sheet_last.nrows:
                    last_list_temp.append(read_sheet_last.cell_value(iter_line - 1, iter_column))
                else:
                    last_list_temp.append(read_sheet_last.cell_value(iter_line, iter_column))

            penultimate_list.append(penultimate_list_temp)
            last_list.append(last_list_temp)

        return penultimate_list, last_list
    else:
        print("Для анализа данных необходимо минимум 2 листа данных!!!")
        save()


def comparison():
    penultimate_, last_ = data_extraction()
    for val_penultimate in penultimate_:
        for val_last in last_:
            if val_penultimate != val_last:
                print(val_penultimate)


if __name__ == "__main__":
    comparison()
