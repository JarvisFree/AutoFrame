#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    ：2021/4/9 23:58
@Author  ：维斯
@File    ：py_util_json.py
@Version ：1.0
@Function：JSON工具
"""

import json


class PyUtilJson:
    @staticmethod
    def json_format(json_str, is_dict_str=False):
        """
        格式化JSON字符串
        :param json_str: 原始json字符串(双引号 非字典的单引号)
        :param is_dict_str: json_str是否是字典字符串
        :return: 格式化后的JSON字符串（JSON格式形式）
        """
        # 验证是否是str类型
        if type(json_str) != str:
            json_str = str(json_str)
        # 若json_str是字典字符串
        if is_dict_str:
            json_str = json_str.replace('\'', '\"')
        json_str = json.loads(json_str)
        return json.dumps(json_str, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)

    @staticmethod
    def get_params_to_json_params(get_params_str):
        """
        GET请求中的参数转换为JSON格式
        :param get_params_str:
        """
        """
        如：password=123456&tel=13675480983 转换为
        {
            "password": "123456",
            "tel": "13675480983"
        }
        """
        params = get_params_str.split('&')
        params_json = {}
        for count in range(len(params)):
            a = params[count].split('=')
            params_json[a[0]] = a[1]
        print(json.dumps(params_json, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False))
        return json.dumps(params_json)

    @staticmethod
    def json_params_to_get_params(json_params_str):
        """
        JSON格式/字典格式 转换为GET请求中的参数
        :param json_params_str:
        """
        """
        如：
        {
            "password": "123456",
            "tel": "13675480983"
        }
        转换为
        password=123456&tel=13675480983
        """
        # 判断是否是字符串类型
        if type(json_params_str) != str:
            json_params_str = str(json_params_str)
        # 字典字符串 转换 json字符串
        json_params = json_params_str.replace('\'', '\"')
        # json转换为字典
        dict_params = json.loads(json_params)
        get_params = ''
        for key, value in dict_params.items():
            get_params = '{}{}={}&'.format(get_params, key, value)
        # 去除最后一个‘&’
        get_params = get_params[:len(get_params) - 1]
        print(get_params)
        return get_params

    @staticmethod
    def header_to_json(header: str):
        """
        :param header:

        如：
        accept: */*\r\n\
        accept-encoding: gzip, deflate, br
        accept-language: zh-CN,zh;q=0.9
        content-length: 592
        content-type: application/json
        origin: https://abc.aaa.net
        referer: https://abc.aaa.net/
        sec-fetch-dest: empty
        sec-fetch-mode: cors
        sec-fetch-site: same-site
        user-agent:
        x-app-version: 1
        x-auth-token
        x-channel: H5
        x-client-ip: 111.111.111.111
        x-device-id: iOS|iPhone|Safari|605.115
        x-tenant-code: 101

        转为json格式
        {
            "accept":"*/*",
            "accept-encoding":"gzip, deflate, br",
            "accept-language":"zh-CN,zh;q=0.9",
            "content-length":"592",
            "content-type":"application/json",
            "origin":"https://abc.aaa.net",
            "referer":"https://abc.aaa.net/",
            "sec-fetch-dest":"empty",
            "sec-fetch-mode":"cors",
            "sec-fetch-site":"same-site",
            "user-agent":"",
            "x-app-version":"1",
            "x-auth-token":"",
            "x-channel":"H5",
            "x-client-ip":"111.111.111.111",
            "x-device-id":"iOS|iPhone|Safari|605.115",
            "x-tenant-code":"101"
        }

        :return JSON格式的请求头
        """
        header_json = {}
        # step1 获取每个header （\r\n区分）
        header_list = header.split('\r\n')
        for header in header_list:
            # 提取key、value
            h = header.split(': ')
            if len(h) == 1:
                h.append('')
            # 删除空格
            # h[0] = h[0].replace(' ', '')
            # h[1] = h[1].replace(' ', '')
            header_json[h[0]] = h[1]
        # JSON格式化
        json_str = PyUtilJson().json_format(str(header_json), True)
        print(json_str)
        return json_str


if __name__ == '__main__':
    str1 = 'page={}&num=100&sort=symbol&asc=1&node={}&symbol=&_s_r_a=init'
    PyUtilJson().get_params_to_json_params(str1)
