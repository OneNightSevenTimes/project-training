from .base import Baseplugin
import traceback
from lib import response
class Nicplugin(Baseplugin):
    def linux(self):
        '''
        执行命令，获取资产信息
        :return:
        '''
        ret = {'status':True,'data':None,'error':None}
        ret = response.BaseResponse()
        try:
            result = self.cmd('nic')
            ret.data = result
        except Exception as e:
            ret.status = False
            ret.error = traceback.format_exc()
        return ret