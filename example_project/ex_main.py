#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    ：2021/6/19 12:59
@Author  ：维斯
@File    ：ex_main.py
@Version ：1.0
@Function：
"""

from frame.control.control import Control
from common.py_util_pro_path import PyUtilProPath

if __name__ == '__main__':
    root_path = f'{PyUtilProPath.project_root_path(print_log=False)}example_project'
    ''' 1 文件路径 '''
    # 接口数据文件
    data_file = f'{root_path}\\data\\ex_data.xls'
    # 输出测试记录文件
    record_file = f'{root_path}\\record\\ex_record.xls'

    ''' 2 使用框架 '''
    con = Control()
    # 接口所在的sheet表名称
    interface_sheet_name = '新浪财经行情中心'
    # 接口名称
    interface_name = '获取股票数据'
    # 接口请求
    con.invoke(
        interface_name=interface_name, excel_file=data_file, update_interface_sheet_name=interface_sheet_name
    )
    # 输出测试记录
    con.build_test_record(record_file)
