from odps import ODPS
from odps.df import DataFrame


def get_odps(access_id, access_key, project_name, endpoint):
    o = ODPS(access_id=access_id,
             secret_access_key=access_key,
             project=project_name,
             endpoint=endpoint
             )

    return o


def get_table(o, table_name):
    return DataFrame(o.get_table(table_name))


def excute_sql(o, sql):
    reader = o.execute_sql(sql).open_reader()
    print(reader)
    for record in reader:
        print(record)


if __name__ == '__main__':
    access_id = 'NE5RYcFUSOkzSUQK'
    access_key = 'gmQxEPpXfYXd7BCwQQUM3OxvpmZwRn'
    project_name = 'city_brain'
    endpoint = 'http://service.cn-shanghai-shga-d01.odps.ops.ga.sh/api'

    table_name = 'dim_signaloptim_inter_info'

    odps = get_odps(access_id, access_key, project_name, endpoint)
    table = get_table(odps, table_name)

    sql = """select * from ods_rdnet_signalight_info_jiaojing where dt='20191125' and cust_signal_id like '120%'"""
    excute_sql(odps, sql)

    # print(table.schema)
