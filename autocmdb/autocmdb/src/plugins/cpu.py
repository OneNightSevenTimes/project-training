from .base import Baseplugin
import traceback
from lib import response
import logging
from lib import logger_helper
from config import settings
import os

class Diskplugin(Baseplugin):
    def linux(self):
        '''
        执行命令，获取资产信息
        :return:
        '''
        ret = response.BaseResponse()
        try:
            if self.test_mode:
                result = open(os.path.join(settings.BASE_DIR,'files/cpuinfo.out'),'r').read()
            else:
                shell_command = 'cat /proc/cpuinfo'
                result = self.cmd(shell_command)
            ret.data = result
        except Exception as e:
            ret.status = False
            ret.error = traceback.format_exc()
            obj = logger_helper.LoggerHelper.instance()
            obj.error_logger.log(logging.FATAL,ret.error)
        return ret