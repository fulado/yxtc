# wgs84 地球坐标系 国际通用
# GCJ02 火星坐标系 中国
import csv
import string
import time
import math

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


# gcj transform to bd2
def gcj2bd(lat, lon):
    x = lon
    y = lat
    z = math.sqrt(x * x + y * y) + 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) + 0.000003 * math.cos(x * x_pi)
    bd_lon = z * math.cos(theta) + 0.0065
    bd_lat = z * math.sin(theta) + 0.006
    bdpoint = [bd_lon, bd_lat]
    return bdpoint


# wgs transform to bd
def wgs2bd(lat, lon):
    wgs_to_gcj = wgs2gcj(lat, lon)
    gcj_to_bd = gcj2bd(wgs_to_gcj[0], wgs_to_gcj[1])
    return gcj_to_bd;


# for i in range(3, 4):
#     n = str('2017.040' + str(i) + '.csv')
#     m = str('2017040' + str(i) + '.csv')
#     csvfile = open(m, 'w', encoding='UTF-8', newline='')
#     nodes = csv.writer(csvfile)
#     nodes.writerow(['md5', 'content', 'phone', 'conntime', 'recitime', 'lng', 'lat'])
#     l = []
#     with open(n, newline='', encoding='UTF-8') as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             if row['md5'] == 'md5':
#                 continue
#             else:
#                 y = float(row['lng'])
#                 x = float(row['lat'])
#                 loc = wgs2bd(x, y)
#                 l.append([row['md5'], row['content'], row['phone'], row['conntime'], row['recitime'], loc[0], loc[1]])
#     nodes.writerows(l)
#     csvfile.close()
#
#     print("转换成功")

if __name__ == '__main__':
    pos_84 = (31.28522467460700000000, 121.45030080444000000000)
    pos_gcj = wgs2gcj(pos_84[0], pos_84[1])
    print(pos_gcj)




