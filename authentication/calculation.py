import xlrd
def calculate_capacity(vehicle_name, charge):
    location = "C:\\Users\\kalai\\Desktop\\projects for iv year\\dataset\\FEV data.xls"
    var_workbook = xlrd.open_workbook(location)
    sht = var_workbook.sheet_by_index(0)
    row = sht.nrows
    col = sht.ncols
    vehi = []
    row = sht.nrows
    col = sht.ncols 
    
    for i in range(row):
        for j in range(col):
            index = sht.cell_value(i, j)
            if index == vehicle_name:
                range_value = sht.cell_value(i, j+7)
                capacity = (range_value * int(charge)) / 100
                vehi.append(capacity)
    
    return vehi
