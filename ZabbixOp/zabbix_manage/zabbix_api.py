#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib2 import URLError
from django.conf import settings
from ZabbixOp.settings import logger

import json
import urllib2
import ConfigParser
import sys,os.path
import time

"""
    1.批量添加主机,指定主机组,指定模板
    2.批量添加主机,指定模板,指定不同的组
    3.批量对一批主机关联新的模板,但是这些主机在不同组
    需要用到的method:
        host.get
        template.get
        hostgroup.get
        host.update
        host.create
"""
os.environ['DJANGO_SETTINGS_MODULE'] = 'ZabbixOp.settings'
if sys.version_info[0] < 3 and sys.version_info[1] <= 7:
    reload(sys)
    sys.setdefaultencoding('utf8')

###读取配置文件
config_dir = os.path.join(settings.BASE_DIR,'zabbix.cfg')
print(config_dir)
config = ConfigParser.ConfigParser()
config.read(config_dir)
sections = config.sections()

try:
    url = config.get('zabbix','url')
    username = config.get('zabbix','username')
    password = config.get('zabbix','password')
except Exception as e:
    if hasattr(e,'reason'):
        logger.error(e.reason)
        print(e.reason)
    elif hasattr(e,'code'):
        logger.error("Error Code:%s" %(e.code))
        print(e)

def mylogging(content,level="INFO"):
    RealTime = time.strftime("%y-%m-%d %H:%M:%S",time.localtime())
    with open('./zabbix.log','a') as file:
        text = RealTime + " - " + str(level) + "-"  + str(content) + "\n"
        file.write(text)
#url = "http://10.69.213.86/zabbix/api_jsonrpc.php"
#username = 'wangyichen'
#password = 'wangyichen'
#url="http://zabbix.intra.gomeplus.com/zabbix/api_jsonrpc.php"
#username = 'apiadd'
#password = 'apiadd'

class Zabbix(object):
    """
        基于zabbix http api封装
    """
    def __init__(self):
        self.url = url
        self.header = {"Content-Type": "application/json"}
        self.token = self.user_login()

    def user_login(self):
        data = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": username,
                "password": password
            },
            "id": 1,
        }
        data = json.dumps(data)
        request = urllib2.Request(self.url,data)
        request.headers.update(self.header)
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            logger.error("Auth Failed,Please Check Your Name and Password!")
        else:
            response = json.loads(result.read())
            result.close()
            if not response.has_key('result'):
                raise KeyError(response)
            else:
                tokenID = response['result']
                return tokenID

    def post_data(self,data):
        """
        :param data:zabbix api 请求的参数
        :param hostip:
        :return:
        """
        request = urllib2.Request(self.url,data)
        request.headers.update(self.header)
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            if hasattr(e,'reason'):
                logger.error(e.reason)
                print(e)
            elif hasattr(e,'code'):
                logger.error("Error Code:%s" %(e.code))
            return 0
        else:
            response = json.loads(result.read())
            result.close()
            return response

    def get_hostinfo(self,*hostip):
        """
        :param hostip:通过ip获取主机信息
        :return:主机信息列表
            hostid
            hostname
            hostip
            status

        """
        data = json.dumps(
                {
                    "jsonrpc": "2.0",
                    "method": "host.get",
                    "params": {
                        "output":["hostid","name","available","host"],
                        "filter": {"ip": list(hostip)},
                        "selectInterfaces":[
                            'ip'
                        ],
                        "selectParentTemplates": [
                            "templateid",
                            "name"
                        ],
                    },
                    "auth": self.token,
                    "id": 1
        })
        response = self.post_data(data)
        result = response['result']
        res = []
        if response != 0 and len(result) !=0:
            for hostinfo in result:
                if hostinfo['available'] == '0':   #状态未监控
                    info = {
                        'HostId': hostinfo['hostid'],
                        'HostIp': hostinfo['interfaces'][0]['ip'],
                        'HostName': hostinfo['name'],
                        'available': "Monitoring"
                    }
                    res.append(info)
                elif hostinfo["available"] == '1':  #状态监控中
                    info = {
                        'HostId': hostinfo['hostid'],
                        'HostIp': hostinfo['interfaces'][0]['ip'],
                        'HostName': hostinfo['name'],
                        'available': "Not Monitored"
                    }
                    res.append(info)
            return res
        else:
            logger.warning("Get Host Error or cannot find this host,please check !")
            return res

    def get_hostlist(self):
        pass

    def del_host(self,*hostip):
        """
        :param hostip:通过Ip删除主机
        :return:
        """
        print(hostip)
        host_infos = self.get_hostinfo(*hostip)
        print(host_infos)
        if len(host_infos) < len(hostip):   #判断返数是否和要删除的IP数相等
            result_ips = [info['HostIp']for info in host_infos]
            NotFoundIp = [ip for ip in hostip if ip not in result_ips]
            logger.error(str(NotFoundIp) + ' Ip Not Found!')
            return str(NotFoundIp) + ' Ip Not Found!'     #返回不存在的ip

        else:
            hostid = [ host_id['HostId'] for host_id in self.get_hostinfo(*hostip)]
            data = json.dumps({
                "jsonrpc":"2.0",
                "method":"host.delete",
                "params":hostid,
                "auth":self.token,
                'id':1,
            })
            result = self.post_data(data)
            result = result['result']
            if "hostids" in result.keys():
                logger.info("delete %s success" %(str(hostip)))
                return "delete %s success" %(str(hostip))
            else:
                logger.error("delete %s Failed" %(str(hostip)))
                return "delete %s Failed" %(str(hostip))

    def get_hostgroup(self):
        """
        :return: 主机组列表
        """
        data = json.dumps({
            'jsonrpc': '2.0',
            'method': 'hostgroup.get',
            'params': {
                'output':'extend',
            },
            'auth': self.token,
            'id': 1
        })
        response = self.post_data(data)
        print(response)
        if 'result' in response.keys():
            result = response['result']
            res = []
            for host_group in result:
                info = {
                    'GroupName': host_group['name'],
                    'GroupId': host_group['groupid']
                }
                res.append(info)
            return res

    def get_template(self):
        """
        :return: Template List
        """
        data = json.dumps({
            'jsonrpc': '2.0',
            'method': 'template.get',
            'params': {
                'output': 'extend'
            },
            'auth': self.token,
            'id': 1
        })
        response = self.post_data(data)
        if 'result' in response.keys():
            result = response['result']
            res = []
            for template in result:
                info = {
                    'TemplateName': template['name'],
                    'TemplateId': template['templateid']
                }
                res.append(info)
            return res

    def host_exist(self,host):
        """
        :param host:
        :return:
        """
        pass

    def create_host(self,HostIp,HostGroupId,TemplateId,HostName=None):
        """
        :param HostIp:
        :param HostGroupId:
        :param TemplateId:
        :return:
        """
        if HostIp and HostGroupId and TemplateId:
            if HostName is None:
                HostName = HostIp
            data = json.dumps({
                'jsonrpc': '2.0',
                'method': 'host.create',
                'params':{
                        'host': HostName,
                        'interfaces':[
                            {
                                'type': 1,
                                'main': 1,
                                'useip':1,
                                'ip': HostIp,
                                'dns': '',
                                'port': 10050
                            }
                        ],
                        'groups':[
                            {
                                'groupid': int(HostGroupId)
                            }
                        ],
                        "templates": [
                            {
                                "templateid": int(TemplateId)
                            }
                        ]
                    },
                'auth':self.token,
                'id':1
            })
            response = self.post_data(data)
            if 'result' in response:
                result = response['result']
            elif 'error' in response:
                error = response['error']['data']
                mylogging(error)
                return error

    def create_multi_host(self,host_list,group_list,template_list,hostname_list=""):
        result = {
            'success':[],
            'failed':[]
        }
        group_id_params = [ {'groupid':group_id} for group_id in group_list]
        templte_id_params = [{"templateid":template_id} for template_id in template_list]
        ##判断hostname和hostip长度是否一致,否则hostname == hostip
        """
            hostname_list = ['test1','test2']
            host_list = ['11.11.11.11','11.11.11.12','11.11.11.13']
        """
        if len(hostname_list) < len(host_list):
            hostname_list.extend(host_list[len(hostname_list):])
        h = 0
        for host in host_list:
            if not hostname_list[h]:
                hostname_list[h] = host
            data = {
                'jsonrpc': '2.0',
                'method': 'host.create',
                'params':{
                        'host': hostname_list[h],
                        'interfaces':[
                            {
                                'type': 1,
                                'main': 1,
                                'useip':1,
                                'ip': host,
                                'dns': '',
                                'port': 10050
                            }
                        ],
                        'groups':group_id_params,
                        "templates": templte_id_params
                    },
                'auth':self.token,
                'id':1
            }
            h += 1
            response = self.post_data(json.dumps(data))
            if 'result' in response.keys():
                result['success'].append(response['result'])
            else:
                result['failed'].append(response['error']['data'])
        return result

