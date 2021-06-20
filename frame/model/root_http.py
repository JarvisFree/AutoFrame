#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    ：2021/4/11 13:30
@Author  ：维斯
@File    ：root_http.py
@Version ：1.0
@Function：HTTP封装（供框架消费）
"""

import json
import time
import requests
from websocket import create_connection
from common.py_util_json import PyUtilJson
from common.py_util_log import Log


def wrapper_loop_waiting(times=1, sleep=1, print_log=True):
    """
    循环等待装饰器（若func()执行报错 则循环等待）
    :param times: 等待次数
    :param sleep: 每次等待时间（秒）
    :param print_log: 是否打印日志
    :return:
    """

    def wrapper(func):
        def inner_wrapper(*args, **kwargs):
            for i in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if print_log:
                        Log.logger.warning(
                            f'{func.__name__}: 循环等待触发{times}次，每次等待{sleep}秒，当前第{i + 1}次 循环触发原因：{e}'
                        )
                    time.sleep(sleep)

        return inner_wrapper

    return wrapper


class RootHttp:
    type = ['GET', 'POST']
    ws_type = ['WS_GET', 'WS_POST']

    def do_get(
            self, url_get, params_dict=None, headers_dict=None, interface_name='', expect='', global_object: list = None
    ):
        return RootHttp().__request_base(
            self.type[0], url_get, headers_dict=headers_dict, params_dict=params_dict,
            interface_name=interface_name, global_object=global_object, expect=expect
        )

    def do_post(
            self, url_post, params_dict=None, headers_dict=None, interface_name='', expect='', global_object=None
    ):
        return RootHttp().__request_base(
            self.type[1], url_post, headers_dict=headers_dict, params_dict=params_dict,
            interface_name=interface_name, global_object=global_object, expect=expect
        )

    @staticmethod
    def do_ws_get(url_ws_get, headers_dict=None, params_dict=None, result_get: list = None):
        return RootHttp().__request_ws_base(url_ws_get, headers_dict, params_dict, result=result_get)

    @staticmethod
    def do_ws_post(url_ws_post, headers_dict=None, params_dict=None, result_post: list = None):
        return RootHttp().__request_ws_base(url_ws_post, headers_dict, params_dict, result=result_post)

    @staticmethod
    def is_expect(old_str, expect_list_str):
        """
        查找字符串中是否有预期值（常用于校验接口预期返回值）
        :param old_str: 原始字符串
        :param expect_list_str: 预期字符串列表
        :return: 有True；无False
        """
        for expect in expect_list_str:
            # step1 去除单引号、双引号、空格字符、回车、换行
            expect = str(expect)
            str_result = str(old_str)
            str_result = str_result.replace('\"', '').replace('\'', '').replace(' ', '').replace('\r', '').replace('\n',
                                                                                                                   '')
            if str_result.find(expect) == -1:
                return False
        return True

    def __request_base(
            self, request_type, url_com, headers_dict, params_dict, performance=False,
            interface_name='', expect='', global_object: list = None
    ):
        """
        HTTP请求
        :param request_type: 请求类型（GET、POST）
        :param url_com: 请求地址（不含参数）
        :param headers_dict: 请求头
        :param params_dict: 请求参数
        :param performance: 是否是性能测试
        :param interface_name: 接口名称
        :param expect: 预期值
        :param global_object: 全局对象
        :return: 返回请求结果
        """
        # 开关 是否打印接口数据
        is_print = True
        # 开关 返回数据超长 是否截取
        is_sub = False

        # step1 请求
        start_time_s = int(round(time.time() * 1000))
        result_re = ''
        # GET
        if request_type == self.type[0]:
            # 参数拼接到url
            if params_dict != '':
                url_com = url_com + '?'
                for key, value in params_dict.items():
                    url_com = '{}{}={}&'.format(url_com, key, value)
                # 去除最后一个‘&’
                url_com = url_com[:len(url_com) - 1]
            if performance:
                pass
            else:
                result_re = requests.get(url_com, headers=headers_dict, verify=False)

        # POST
        if request_type == self.type[1]:
            # 字段：data     参数：字典
            if headers_dict['content-type'] == 'application/x-www-form-urlencoded':
                result_re = requests.post(url_com, headers=headers_dict, data=params_dict, verify=False)
            # 字段：json     参数：字典
            elif headers_dict['content-type'] == 'application/json':
                result_re = requests.post(url_com, headers=headers_dict, json=params_dict, verify=False)
            else:
                result_re = requests.post(url_com, headers=headers_dict, data=params_dict, verify=False)

        end_time_s = int(round(time.time() * 1000))

        # step2 获取返回数据
        result_format = json.loads(result_re.content.decode('utf-8'))
        params_dict = PyUtilJson.json_format(json.dumps(params_dict))

        # step3 打印接口数据
        out = PyUtilJson.json_format(json.dumps(result_format))
        if is_print:
            print('=================={} 请求耗时：{}(ms)========================'.format(interface_name,
                                                                                    end_time_s - start_time_s))
            print('请求方式：{}'.format(request_type))
            print('URL：{}'.format(url_com))
            print('请求头：{}'.format(headers_dict))
            print('入参：\r\n{}'.format(params_dict))
            if is_sub:
                if len(out) < 1000:
                    print('出参：\r\n{}'.format(out))
                else:
                    out_str = out[:500]
                    out_str += '****************长度大于1000个字符 仅显示前500位、后500位****************' + out[-500:]
                    print('出参：\r\n{}'.format(out_str))
            else:
                print('出参：\r\n{}'.format(out))
            print('===========================================================')

        # step4 接口数据存入全局变量（序号、接口名称、接口地址、请求方式、请求头、请求参数、返回参数、请求耗时、预期返回、测试结果）
        expect_result = str(expect).split('\n')  # 预期结果字符串 以回车换行作为区分
        count = len(global_object)
        interface_list = [
            count + 1,
            interface_name,
            url_com,
            request_type,
            headers_dict,
            params_dict,
            out,
            end_time_s - start_time_s,
            expect,
            'PASS' if self.is_expect(result_format, expect_result) else 'NOT PASS'
        ]
        global_object.append(interface_list)
        Log.logger.info('添加全局接口数据：{}'.format(interface_list))
        return result_re

    @staticmethod
    def __request_ws_base(url_ws_com, headers_dict=None, params_dict=None, result: list = None, request_times=10):
        """
        websocket请求
        :param url_ws_com:
        :param headers_dict:
        :param params_dict:
        :param result:
        :param request_times: 接口请求次数
        """

        @wrapper_loop_waiting(times=20, sleep=10)
        def ws_loop(header_dict, url):
            if header_dict is not None:
                ws_con = create_connection(url, header=header_dict)
            else:
                ws_con = create_connection(url)
            return ws_con

        ws = ws_loop(headers_dict, url_ws_com)
        if ws.status == 101:
            Log.logger.info(f'请求成功：{url_ws_com}')
        else:
            Log.logger.warning(f'请求失败：{url_ws_com}')
        for i in range(request_times):
            if params_dict is not None:
                params = params_dict
                ws.send(str(params))
            response = ws.recv()
            if result is not None:
                result.append(response)
            print(response)
        ws.close()


if __name__ == '__main__':
    pass
