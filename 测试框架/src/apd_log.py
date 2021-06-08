# coding=utf-8
'''
Created on 2017-9-25

@author: zhuofuliu
'''
import datetime
import threading
import sys
import traceback


class ApdLog(object):

    # 日志级别
    DEBUG = 1
    INFO = 2
    ERROR = 3
    SYS = 4

    log_level = INFO

    lock = threading.RLock()

    @classmethod
    def set_level(cls, level):
        if level >= cls.DEBUG and level <= cls.SYS:
            cls.log_level = level

    @classmethod
    def log(cls, level, flag, content):
        '''
        用例编写不可调用
        '''
        if level < cls.log_level:
            return

        t = datetime.datetime.now().strftime('[%H:%M:%S.%f')[:-3] + ']'
        if isinstance(content, type(u'')):
            content = content.encode('utf8', 'ignore')
        logstr = t + flag + " " + content
        cls.lock.acquire()
        print logstr
        if level == cls.ERROR:
            s = traceback.format_stack()
            print cls.apd_fmt_stack(s)
        sys.stdout.flush()
        cls.lock.release()

    @classmethod
    def apd_fmt_stack(cls, s):
        new_s = []
        for one_s in s:
            if '\\runpy.py' in one_s or '/runpy.py' in one_s:
                continue
            if '\\unittest\\' in one_s or '/unittest/' in one_s:
                continue
            if 'src\\apd_log.py' in one_s or 'src/apd_log.py' in one_s:
                continue
            if 'src\\apd_testcase.py' in one_s or 'src/apd_testcase.py' in one_s:
                continue
            new_s.append(one_s)

        return ''.join(new_s)

    @classmethod
    def log_error(cls, content):
        '''
        打印error日志
        '''
        ApdLog.log(cls.ERROR, '[error]', content)

    @classmethod
    def log_info(cls, content):
        '''
        打印info日志
        '''
        ApdLog.log(cls.INFO, '[info] ', content)

    @classmethod
    def log_debug(cls, content):
        '''
        打印error日志
        '''
        ApdLog.log(cls.DEBUG, '[debug]', content)

    @classmethod
    def log_sys(cls, content):
        '''
        打印sys日志
        '''
        ApdLog.log(cls.SYS, '[sys]  ', content)
