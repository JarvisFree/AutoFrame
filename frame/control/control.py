#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    ：2021/4/10 13:45
@Author  ：维斯
@File    ：control.py
@Version ：1.0
@Function：控制器（连接框架）
"""

from frame.model.root import Root


class Control:
    """
    所有业务自动化 通过此类连接框架 此类是连接框架的唯一桥梁（直接调用此类 不用继承）
    """

    def __init__(self):
        self.__root = Root()

    def invoke(self, interface_name, headers_dict=None, params_dict=None, excel_file=None, update_env_name=None,
               update_interface_sheet_name=None, ws_result: list = None, url_default=None):
        """
        接口请求调用
        :param interface_name: 被测接口名称
        :param headers_dict: 请求头（None 则读取表格数据）
        :param params_dict: 请求参数（None 则读取表格数据）
        :param excel_file: 测试数据文件
        :param update_env_name: 测试环境名称
        :param update_interface_sheet_name: 测试接口sheet表名称
        :param ws_result: ws接口返回的数据存到列表里
        :param url_default: 默认url（如：https://i.cnblogs.com/posts）
        :return: 成功：接口返回结果（字典类型）；失败：False
        """
        return self.__root.request(interface_name=interface_name, headers_dict=headers_dict, params_dict=params_dict,
                                   update_env_file=excel_file, update_env_name=update_env_name,
                                   update_interface_sheet_name=update_interface_sheet_name, ws_result=ws_result,
                                   url_default=url_default)

    def add_global(self, key, value):
        """
        添加全局变量
        :param key:
        :param value:
        """
        self.__root.add_global_value(key=key, value=value)

    def get_global(self, key):
        """
        获取全局变量
        :param key:
        :return:
        """
        return self.__root.get_global_value(key=key)

    def build_test_record(self, record_file):
        """
        生成测试记录（接口测试记录）
        :param record_file: 测试记录文件
        """
        self.__root.interface_record(file=record_file)

    def build_test_report(self):
        pass
