import xlrd
import os

def calculate_capacity(vehicle_name, charge):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    location = os.path.join(BASE_DIR, 'dataset', 'FEV data.xls')

    print("Using file:", location)  # debug

    var_workbook = xlrd.open_workbook(location)
    sht = var_workbook.sheet_by_index(0)

    vehi = []

    for i in range(sht.nrows):
        for j in range(sht.ncols):
            index = sht.cell_value(i, j)
            if index == vehicle_name and j + 7 < sht.ncols:
                range_value = sht.cell_value(i, j+7)
                capacity = (range_value * int(charge)) / 100
                vehi.append(capacity)

    return vehi