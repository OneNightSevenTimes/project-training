from src import plugins
from config import settings
import requests
import json
from concurrent.futures import ThreadPoolExecutor
class Baseclient(object):
    def process(self):
        raise NotImplementedError('派生类必须实现process方法')
    def send(self, info):
        requests.post(
            url=settings.API,
            json= info#先序列化，不这样的话字典不能包含字典
        )

class SubBaseclient(Baseclient):
    def get_hosts(self):
        response = requests.get(settings.API)
        host_list = json.loads(response.text)
        return host_list
    def task(self,host):
        info = plugins.server_info(host)
        self.send(info)
class Agentclient(Baseclient):
    def process(self):
        info = plugins.server_info()
        self.send(info)

class Sshclient(SubBaseclient):
    def process(self):
        host_list = self.get_hosts()
        pool = ThreadPoolExecutor(10)
        for host in host_list:
            pool.submit(self.task,host)


class Saltclient(SubBaseclient):
    def process(self):
        host_list = self.get_hosts()
        pool = ThreadPoolExecutor(10)
        for host in host_list:
            pool.submit(self.task,host)