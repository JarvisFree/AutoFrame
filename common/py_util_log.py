#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    ：2021/4/9 22:11
@Author  ：维斯
@File    ：py_util_log.py
@Version ：1.0
@Function：日志工具
"""

import logging
from common.py_util_pro_path import *


class Log:
    log_file = PyUtilProPath.project_root_path('AutoFrame', print_log=False) + 'log\\日志.log'
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    logger = logging.getLogger('MyLogger')

    logger.setLevel(logging.DEBUG)
    l_f = logging.Formatter(log_format)
    # 输出到控制台
    con_hand = logging.StreamHandler()
    con_hand.setFormatter(l_f)
    # 输出到文件
    file_hand = logging.FileHandler(log_file, encoding='utf-8')
    file_hand.setFormatter(l_f)

    logger.addHandler(con_hand)
    logger.addHandler(file_hand)


if __name__ == '__main__':
    Log.logger.info('11111111111111111')
    Log.logger.warning('222222222222222222')
    Log.logger.debug('3333333333333333')
    Log.logger.error('4444444444444444')
    Log.logger.critical('5555555555555555')
