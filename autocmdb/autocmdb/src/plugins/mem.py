from .base import Baseplugin
import traceback
from lib import response
import logging
from lib import logger_helper
class Memplugin(Baseplugin):
    def linux(self):
        '''
        执行命令，获取资产信息
        :return:
        '''
        ret = response.BaseResponse()
        try:
            result = self.cmd('mem')
            ret.data = result
        except Exception as e:
            ret.status = False
            ret.error = traceback.format_exc()
            obj = logger_helper.LoggerHelper.instance()
            obj.error_logger.log(logging.FATAL,ret.error)
        return ret