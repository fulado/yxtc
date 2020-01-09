from odps import ODPS
from odps.df import DataFrame


if __name__ == '__main__':
    access_id = 'NE5RYcFUSOkzSUQK'
    access_key = 'gmQxEPpXfYXd7BCwQQUM3OxvpmZwRn'
    project_name = 'city_brain'
    # endpoint = 'http://service.cn-shanghai-shga-d01.odps.ops.ga.sh/api'
    endpoint = 'http://15.74.19.77/api'

    o = ODPS(access_id=access_id,
             secret_access_key=access_key,
             project=project_name,
             endpoint=endpoint
             )

    table = DataFrame(o.get_table('dim_signaloptim_inter_info'))

    print(table.schema)
