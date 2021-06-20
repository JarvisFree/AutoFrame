#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    ：2021/4/11 14:25
@Author  ：维斯
@File    ：root.py
@Version ：1.0
@Function：框架核心
"""

import json
import os
import xlrd
from typing import List
from common.py_util_excel import PyUtilExcel
from common.py_util_log import Log
from frame.model.root_http import RootHttp


class Root:

    def __init__(self):
        """ 接口文件 """
        self.__i_file_path = ''

        """ 环境 """
        self.__env_sheet = '环境'  # 环境数据所在的文件sheet表（sheet名称）
        self.__env_name = None  # 被测环境名称（若有配置 则读取使用此值 不使用表格中的"启用"环境值）
        # 环境所在列Index
        self.__ENV_ENABLE_INDEX = 0  # 启用的环境（即：使用哪个环境测试）
        self.__ENV_NAME_INDEX = 1  # 环境名称
        self.__ENV_ADDRESS_INDEX = 2  # 环境地址

        """ 接口 """
        self.__i_sheet = 'XX后台管理系统'  # 被测接口所在的文件sheet表（sheet名称 如：“XX后台管理系统”）
        # 接口各项所在列Index
        self.__I_NUMBER_INDEX = 0  # 序号
        self.__I_NAME_INDEX = 1  # 接口名称
        self.__I_ADDRESS_INDEX = 2  # 接口地址
        self.__I_TYPE_INDEX = 3  # 请求方式
        self.__I_HEADER_INDEX = 4  # 请求头（JSON）
        self.__I_PARAM_INDEX = 5  # 入参（JSON）
        self.__I_RETURN_SAMPLE_INDEX = 6  # 出参示例（JSON 仅供查看）
        self.__I_EXPECT_INDEX = 7  # 断言

        """ 全局变量 """
        self.__global_value = {}  # 全局变量
        self.__global_interface_record: List[list] = []  # [[]] 全局接口数据 用于接口测试记录数据消费

        """ 其他 """
        self.__PROJECT_NAME = 'AutoFrame'  # 项目名称

    def __update_env(self, file=None, env_name=None, interface_sheet_name=None):
        """
        修改环境信息
        :param file: 测试数据文件
        :param env_name: 环境名称
        :param interface_sheet_name: 测试接口sheet表
        """
        if file is not None:
            self.__i_file_path = file
        if env_name is not None:
            self.__env_name = env_name
        if interface_sheet_name is not None:
            self.__i_sheet = interface_sheet_name

    def __get_all_interface_record(self):
        """
        获取接口测试记录
        :return: [[]]
        """
        return self.__global_interface_record

    def __get_xl_env_host(self, sheet_name):
        """
        获取表格环境地址
        :param sheet_name: 表格中环境数据所在的sheet名称
        :return: 表格中启用环境名称对应的host
        """
        wd = xlrd.open_workbook(self.__i_file_path)
        sheet = wd.sheet_by_name(sheet_name)
        # 获取启用环境名称
        enable = sheet.row_values(1)[self.__ENV_ENABLE_INDEX]  # 表格中的环境名称
        if self.__env_name is not None:  # 若代码里有配置读取的环境 则优先读取
            enable = self.__env_name

        # 查找启用环境名称对应的host
        for index in range(sheet.nrows):
            if sheet.row_values(index)[self.__ENV_NAME_INDEX] == enable:
                return sheet.row_values(index)[self.__ENV_ADDRESS_INDEX]
        Log.logger.error(f'{self.__i_file_path} 在sheet表({sheet_name})中，未找到此环境名称({enable})')

    def __get_test_data(self, interface_name):
        """
        获取表格中被测接口测试数据
        :param interface_name: 接口名称
        :return: 接口名称str，接口地址str，请求方式str，请求头dict，请求参数dict，预期返回str
        """
        try:
            wd = xlrd.open_workbook(self.__i_file_path)
            sheet = wd.sheet_by_name(self.__i_sheet)
        except Exception as e:
            Log.logger.error(f'{self.__i_file_path} 文件错误：{e}', stack_info=True)
        # 循环查找接口名称所在行i_index
        i_index = 0
        for index in range(sheet.nrows):
            if sheet.row_values(index)[self.__I_NAME_INDEX] == interface_name:
                i_index = index
        if i_index == 0:  # 没在指定sheet表中找到接口名称
            Log.logger.error(
                f'{self.__i_file_path} 在sheet表({self.__i_sheet})中，未找到此接口名称({interface_name})'
            )
        # 获取请求头（换行符分割多个请求头，冒号分割单个请求头的key与value）
        header_str = sheet.row_values(i_index)[self.__I_HEADER_INDEX]
        headers_dict = {}
        if header_str != '' and header_str != '{}':
            header_str2 = header_str.split('\n')
            for count in range(len(header_str2)):
                h = header_str2[count].split(':')
                headers_dict[h[0]] = h[1]
        # 获取请求参数
        params_str = sheet.row_values(i_index)[self.__I_PARAM_INDEX]
        params_dict = json.loads(params_str)

        # 获取指定接口info信息
        return sheet.row_values(i_index)[self.__I_NAME_INDEX], sheet.row_values(i_index)[self.__I_ADDRESS_INDEX], \
               sheet.row_values(i_index)[self.__I_TYPE_INDEX], headers_dict, params_dict, sheet.row_values(i_index)[
                   self.__I_EXPECT_INDEX]

    def add_global_value(self, key, value):
        """
        添加全局变量
        :param key:
        :param value:
        """
        Log.logger.info('添加全局变量：{}={}'.format(key, value))
        self.__global_value[key] = value

    def get_global_value(self, key):
        """
        获取全局变量
        :param key:
        :return:
        """
        return self.__global_value.get(key)

    def __project_root_path(self):
        """
        获取当前项目根路径
        :return: 根路径
        """
        name = self.__PROJECT_NAME
        project_path = os.path.abspath(os.path.dirname(__file__))
        root_path = project_path[:project_path.find("{}\\".format(name)) + len("{}\\".format(name))]
        Log.logger.info('当前项目根路径：{}'.format(root_path))
        return root_path

    def interface_record(self, file):
        """
        接口测试数据记录至表格文件
        :param file: 表格文件
        """
        header_list = [
            ['序号', 5],
            ['接口名称', 35],
            ['接口地址', 20],
            ['请求方式', 10],
            ['请求头', 20],
            ['请求参数', 20],
            ['返回参数', 20],
            ['请求耗时(ms)', 12],
            ['预期返回', 20],
            ['测试结果', 10]
        ]
        PyUtilExcel(header_list=header_list).write(
            out_file=file, data_body=self.__get_all_interface_record(), sheet_name='测试记录'
        )
        Log.logger.info(f'接口测试数据已记录至表格文件 路径：{file}')

    def request(
            self, interface_name, headers_dict=None, params_dict=None, update_env_file=None,
            update_env_name=None, update_interface_sheet_name=None, ws_result: list = None, url_default=None
    ):
        """
        组装数据并请求
        :param interface_name: 被测接口名称
        :param headers_dict: 请求头（None 则读取表格数据）
        :param params_dict: 请求参数（None 则读取表格数据）
        :param update_env_file: 测试数据文件
        :param update_env_name: 测试环境名称
        :param update_interface_sheet_name: 测试接口sheet表名称
        :param ws_result: ws接口返回的数据存到列表里
        :param url_default: 默认url（如：https://i.cnblogs.com/posts）
        :return: 成功：接口返回结果（字典类型）；失败：False
        """
        # 修改测试环境数据
        self.__update_env(update_env_file, update_env_name, update_interface_sheet_name)

        name, address, re_type, header_excel_dict, param_str, expect = self.__get_test_data(interface_name)
        # step1 组装URL
        url = self.__get_xl_env_host(self.__env_sheet) + address

        if headers_dict is not None:
            header = headers_dict  # 代码数据
        else:
            header = header_excel_dict  # 表格数据

        if params_dict is not None:
            param = params_dict  # 代码数据
        else:
            param = param_str  # 表格数据

        response = ''

        if url_default is not None:
            url = url_default

        # 判断请求头、参数 是否都为字典类型
        if type(param).__name__ == 'dict' and type(header).__name__ == 'dict':
            if re_type == RootHttp().type[0]:
                response = RootHttp().do_get(
                    url_get=url, params_dict=param,
                    headers_dict=header, interface_name=interface_name,
                    global_object=self.__global_interface_record, expect=expect
                )
            elif re_type == RootHttp().type[1]:
                response = RootHttp().do_post(
                    url_post=url, params_dict=param,
                    headers_dict=header, interface_name=interface_name,
                    global_object=self.__global_interface_record, expect=expect
                )
            elif re_type == RootHttp().ws_type[0]:
                response = RootHttp().do_ws_get(
                    url_ws_get=url, params_dict=param, headers_dict=header, result_get=ws_result
                )
            elif re_type == RootHttp().ws_type[1]:
                response = RootHttp().do_ws_post(
                    url_ws_post=url, params_dict=param, headers_dict=header, result_post=ws_result
                )

        else:
            Log.logger.error(
                f'非字典类型错误 预期：请求头、参数均为字典类型，'
                f'实际：header_type:{type(header).__name__} param_type:{type(param).__name__}'
            )

        result_dict = json.loads(response.content.decode('utf-8'))

        # 校验接口是否成功（校验返回状态码）
        if response.status_code == 200 or response.status_code == 101:
            return result_dict
        else:
            Log.logger.warning('{} 接口请求失败'.format(interface_name))
            return False
