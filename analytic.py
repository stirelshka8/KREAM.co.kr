import xlrd
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
read_book = xlrd.open_workbook(f"{config['CONFIG']['save']}.xlsx")
number_sheets = (len(read_book.sheet_names()) - 1)  # Единица вычитается, так как отсчет идет с 0
sheet_name = f"{config['CONFIG']['save_analytics']}"
read_sheet_penultimate = read_book.sheet_by_index(number_sheets - 1)
read_sheet_last = read_book.sheet_by_index(number_sheets)


def data_extraction():
    if len(read_book.sheet_names()) > 2:
        penultimate_list = []
        last_list = []
        for iter_line in (range(1, max(read_sheet_penultimate.nrows, read_sheet_last.nrows))):
            penultimate_list_temp = []
            last_list_temp = []

            for iter_column in range(0, 7):
                if iter_line >= read_sheet_penultimate.nrows:
                    penultimate_list_temp.append(read_sheet_penultimate.cell_value(iter_line - 1, iter_column))
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


def comparison():
    penultimate_, last_ = data_extraction()
    last_step = 0

    while last_step < len(max(penultimate_, last_)):
        for step in range(0, len(max(penultimate_, last_))):
            if penultimate_[step] != last_[last_step]:
                print(last_step)
                print(step)
            last_step += 1






if __name__ == "__main__":
    comparison()
