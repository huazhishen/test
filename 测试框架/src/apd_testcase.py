# coding=utf-8
'''
Created on 2017-9-25

@author: zhuofuliu
'''
import unittest
import os
import traceback
import sys
from .apd_log import ApdLog


class ApdTestCase(unittest.TestCase):
    '''
    apdtest平台python用例的基类，所有的用例必须继承自这个类
         用例中所有调用的接口必须是父类的方法，不能直接调用其他模块的方法
    '''

    # 定义用例的常量
    STATE_UNINIT = 1
    STATE_RUN = 2
    STATE_DONE = 3

    RESULT_PASS = 0
    RESULT_FAIL = 1

    def __init__(self, params):
        '''
        定义用例相关变量
        '''
        super(ApdTestCase, self).__init__(params)
        self.state = self.STATE_UNINIT
        self.result = self.RESULT_PASS

        # 解析平台传入参数
        for arg in sys.argv:
            if arg.startswith('--conf_file='):
                self.conf_file = arg[len('--conf_file='):]
            else:
                self.conf_file = None

            if arg.startswith('--thread_id'):
                self.thread_id = arg[len('--thread_id'):]
            else:
                self.thread_id = None

    def before_test(self):
        '''
        用例开发可重写此方法
        用例执行前环境准备，数据准备
        在run_test之前调用
        '''
        pass

    def run_test(self):
        '''
        用例开发重写此方法
        用例的执行逻辑
        before_test在本方法之前执行
        无论本方法执行是否成功，之后都会执行after_test
        '''
        pass

    def after_test(self):
        '''
        用例开发重写此方法
        用例数据清除，环境恢复
        无论run_test执行结果如何，之后都会执行本方法
        '''
        pass

    def setUp(self):
        '''
        用例编写禁止重写此方法
        用例执行前准备请重写before_test方法
        '''
        # 调用before_test
        print ''
        self.log_sys("before_test() begin")
        self.before_test()
        self.log_sys("before_test() end")

    def testRun(self):
        '''
        用例编写禁止重写此方法
        用例执行逻辑请重写run_test方法
        '''
        # 能进入testRun方法，则setUp方法一定是成功的

        # 修改用例状态和结果
        self.state = self.STATE_RUN
        self.result = self.RESULT_PASS

        # 3 调用run_test方法，执行用例逻辑
        self.log_sys("run_test() begin")
        try:
            self.run_test()
        except AssertionError as e:
            # 如果不是unittest框架的异常，则直接抛出
            if not self.is_unittest_exception():
                raise e

            assertMsg = str(e)
            self.log_error(assertMsg)
            s = traceback.format_exc()
            print s
            self.result = self.RESULT_FAIL

        self.log_sys("run_test() end")

        # 4 设置用例状态为完成
        self.state = self.STATE_DONE

    def tearDown(self):
        '''
        用例编写禁止重写此方法
        用例数据清除，环境回复，请重写after_test方法
        '''
        if self.state == self.STATE_DONE:
            if self.result == self.RESULT_FAIL:
                self.log_sys("case set fail, [  FAILED  ]")
            else:
                # state为done，且没有被设置为fail，则用例执行成功
                self.log_sys("case run succ, [  PASSED  ]")

        # 执行after_test
        self.log_sys("after_test() begin")
        self.after_test()
        self.log_sys("after_test() end")

        # 如果state为done，after_test也成功，说明是run_test方法未发生异常
        if self.state == self.STATE_DONE:
            self.log_sys("Global test environment tear-down")

    def set_fail(self, msg=None):
        '''
        用例编写可调用
        设置用例状态为失败，并中止用例执行
        msg: 失败的说明，可选参数
        '''
        self.result = self.RESULT_FAIL
        if msg is None:
            self.fail("by call set_fail()")
        else:
            self.fail(msg)

    def log_error(self, content):
        '''
        用例编写可调用
        打印error日志
        '''
        ApdLog.log_error(content)

    def log_info(self, content):
        '''
        用例编写可调用
        打印info日志
        '''
        ApdLog.log_info(content)

    def log_debug(self, content):
        '''
        用例编写可调用
        打印debug日志
        '''
        ApdLog.log_debug(content)

    def set_log_level(self, level):
        '''
        设置当前的日志级别
        ApdLog.DEBUG
        ApdLog.INFO
        ApdLog.ERROR
        '''
        ApdLog.set_level(level)

    def log_sys(self, content):
        '''
        不可调用
        打印sys日志
        '''
        ApdLog.log_sys(content)

    def is_unittest_exception(self):
        '''
        判断是否为unittest框架抛出的AssertionError
        '''
        flag = os.sep + 'unittest' + os.sep + 'case.py'
        callstack = traceback.format_exc()
        if callstack.find(flag) != -1:
            return True
        else:
            return False
