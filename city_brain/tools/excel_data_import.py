"""
转换excle数据格式为可以直接拷贝到odps中的数据格式
"""


import xlrd
import math

# from .gps_convert import wgs2gcj

# 系数常量
a = 6378245.0
ee = 0.00669342162296594323
x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626


# 转换经度
def transform_lat(x, y):
    ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x))
    ret += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(y * math.pi) + 40.0 * math.sin(y / 3.0 * math.pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(y / 12.0 * math.pi) + 320 * math.sin(y * math.pi / 30.0)) * 2.0 / 3.0
    return ret


# 转换纬度
def transform_lon(x, y):
    ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x))
    ret += (20.0 * math.sin(6.0 * x * pi) + 20.0 * math.sin(2.0 * x * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(x * pi) + 40.0 * math.sin(x / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(x / 12.0 * pi) + 300.0 * math.sin(x / 30.0 * pi)) * 2.0 / 3.0
    return ret


# Wgs transform to gcj
def wgs2gcj(lat, lon):
    dLat = transform_lat(lon - 105.0, lat - 35.0)
    dLon = transform_lon(lon - 105.0, lat - 35.0)
    radLat = lat / 180.0 * pi
    magic = math.sin(radLat)
    magic = 1 - ee * magic * magic
    sqrtMagic = math.sqrt(magic)
    dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * pi)
    dLon = (dLon * 180.0) / (a / sqrtMagic * math.cos(radLat) * pi)
    mgLat = lat + dLat
    mgLon = lon + dLon
    loc = [mgLat, mgLon]
    return loc


def get_excel_data_video(file_name):
    # open excel file
    workbook = xlrd.open_workbook(file_name)

    # get sheet1
    worksheet = workbook.sheets()[0]

    content_list = []

    for i in range(1, worksheet.nrows):
        str_out = ''
        value_list_1 = []
        value_list_2 = []
        for j in range(worksheet.ncols):
            cell_value = str(worksheet.cell_value(i, j)).replace(' ', '')

            if j < 4:
                value_list_1.append(str(cell_value))
            else:
                # print(cell_value)
                value_list_2.append(float(cell_value))
        # print(value_list_1)
        # print(value_list_2)
        pos_convert = wgs2gcj(value_list_2[1], value_list_2[0])
        # print(pos_convert)
        value_list_1.append(str(pos_convert[1]))
        value_list_1.append(str(pos_convert[0]))

        j = 0
        for cell_value in value_list_1:
            if j == 0:
                str_tmp = '("' + cell_value + '", '
            elif j == 5:
                str_tmp = '"' + cell_value + '"),\r'
            else:
                str_tmp = '"' + cell_value + '", '

            j += 1
            str_out += str_tmp

        content_list.append(str_out)

    return content_list


def get_excel_data(file_name):
    # open excel file
    workbook = xlrd.open_workbook(file_name)

    # get sheet1
    worksheet = workbook.sheets()[0]

    content_list = []

    for i in range(1, worksheet.nrows):
        str_out = ''
        for j in range(worksheet.ncols):
            cell_value = str(worksheet.cell_value(i, j))
            cell_value = cell_value.replace('.0', '') if j in (1, 2, 3, 10, 9, 13, 7, 8) else cell_value
            # cell_value = cell_value.replace('.0', '')

            if j == 0:
                str_tmp = '("' + cell_value + '", '
            elif j == worksheet.ncols - 1:
                if i == worksheet.nrows - 1:
                    str_tmp = '"' + cell_value + '");'
                else:
                    str_tmp = '"' + cell_value + '"),\r'
            else:
                str_tmp = '"' + cell_value + '", '

            str_out += str_tmp

        content_list.append(str_out)

    return content_list


def output_to_file(file_name, content_list):
    file = open(file_name, mode='w')

    file.writelines(content_list)

    file.close()

    print('写入完成')


def main():
    # read_file_name = 'E:/city_brain/30_1030/03_一机一档/jiading.xlsx'
    # read_file_name = 'E:/city_brain/30_1030/01_设备挂接/signal/roadnet_tp_device_嘉定区信号机补充_1108.xlsx'
    # read_file_name = 'E:/city_brain/30_1030/01_设备挂接/video/roadnet_tp_device_崇明二期摄像头_1021.xlsx'
    # read_file_name = 'E:/city_brain/30_1030/01_设备挂接/bynt/roadnet_tp_device_金山区卡口_1031.xlsx'
    # read_file_name = 'E:/city_brain/30_1030/04_信号机/cust_inter.xlsx'
    # read_file_name = 'E:/city_brain/30_1030/01_设备挂接/coil/roadnet_tp_device_lane_direction_嘉定区线圈.xlsx'
    # read_file_name = 'E:/city_brain/010151_崇明/devc/video.xlsx'
    read_file_name = 'E:/city_brain/310114_嘉定/devc/radar_cd_fin2.xlsx'

    write_file_name = read_file_name.replace('xlsx', 'txt')

    content_list = get_excel_data(read_file_name)
    # content_list = get_excel_data_video(read_file_name)

    output_to_file(write_file_name, content_list)


if __name__ == '__main__':
    main()



