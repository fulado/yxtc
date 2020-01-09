from odps import ODPS

import os
import base64
import xlwt
import pprint


# 读取图片文件, 并做base64编码
def read_file(file_path):
    file = open(file_path, 'rb')

    return base64.b64encode(file.read()).decode()


# 写入数据到excel文件
def export_to_excel(data_list):
    # 创建工作簿
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('sheet1', cell_overwrite_ok=True)

    # 设置表头
    title = ['inter_id', 'phase_name', 'phase_state', 'file_content']

    # 生成表头
    len_col = len(title)
    for i in range(0, len_col):
        ws.write(0, i, title[i])

    # 写入车辆数据
    i = 1
    for data in data_list:
        ws.write(i, 0, data['inter_id'])
        ws.write(i, 1, data['phase_name'])
        ws.write(i, 2, data['phase_state'])
        ws.write(i, 3, data['file_content'])
        i += 1

    # 将文件保存在内存中
    wb.save(r'D:\phase_pic.xls')


def get_phase_pic_data(file_path, pic_list):
    dir_list = os.listdir(file_path)

    for dir_name in dir_list:
        dir_path = file_path + '/' + dir_name
        file_list = os.listdir(dir_path)

        for file_name in file_list:
            file_name = dir_path + '/' + file_name
            save_pic_data_to_dic(file_name, pic_list)


def get_phase_pic_data_qingpu(file_path, pic_list):
    file_list = os.listdir(file_path)

    for file_name in file_list:
        file_name = file_path + '/' + file_name
        # print(file_name)
        save_pic_data_to_dic_qingpu(file_name, pic_list)


def save_pic_data_to_dic(file_name, pic_list):
    if 'png' in file_name.lower():
        file_info = file_name.split('/')[-1].split('-')
        if len(file_info) < 3:
            print(file_info)

        inter_id = file_info[0]
        phase_name = file_info[-1][0]
        phase_state = file_info[-1][1]
        # print(inter_id, phase_name, phase_state)

        file_content = read_file(file_name)
        # print(file_content)

        pic_info = [inter_id, phase_name, phase_state, file_content]

        pic_list.append(pic_info)
    else:
        pass


def save_pic_data_to_dic_qingpu(file_name, pic_list):
    if 'png' in file_name.lower():
        file_info = file_name.split('/')[-1].split('_')
        if len(file_info) < 3:
            print(file_info)

        if file_info[-1][0] != 'Y':
            inter_id = file_info[0]
            phase_name = file_info[1][0]
            phase_state = file_info[-1][0]
            # print(inter_id, phase_name, phase_state)

            file_content = read_file(file_name)
            # print(file_content)

            pic_info = [inter_id, phase_name, phase_state, file_content]

            pic_list.append(pic_info)
        else:
            pass
    else:
        pass


def write_data_into_odps(table_name, area_name, pic_list):

    # odps链接信息
    # access_id = 'NE5RYcFUSOkzSUQK'
    # access_key = 'gmQxEPpXfYXd7BCwQQUM3OxvpmZwRn'
    # project_name = 'city_brain'
    # endpoint = 'http://service.cn-shanghai-shga-d01.odps.ops.ga.sh/api'

    access_id = 'gxwFKef4XWvSXS9V'
    access_key = 'LcUVj1PRGR02isRX5awP6Me32Rb6Ey'
    project_name = 'jj_znjt'
    endpoint = 'http://service.cn-shanghai-shga-d01.odps.ops.ga.sh/api'

    o = ODPS(access_id=access_id,
             secret_access_key=access_key,
             project=project_name,
             endpoint=endpoint
             )

    # 获取表
    t = o.get_table(table_name)

    # 写入数据
    with t.open_writer(partition='area_name=%s' % area_name, create_partition=True) as writer:
        records = pic_list

        writer.write(records)


def main():
    # 根据不同区的相位图文件位置和名称修改file_path和area_name
    file_path = 'E:/city_brain/010151_崇明/崇明二相位'
    area_name = 'chongming'

    table_name = 'ods_tfc_ctl_signal_phase_pic_city_brain'
    pic_list = []

    get_phase_pic_data(file_path, pic_list)

    # get_phase_pic_data_qingpu(file_path, pic_list)
    # pprint.pprint(pic_list)

    write_data_into_odps(table_name, area_name, pic_list)


if __name__ == '__main__':
    main()
