#coding=utf-8

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import login,authenticate,logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import  login_required
from django.shortcuts import resolve_url
from zabbix_manage.zabbix_api import Zabbix
from zabbix_manage.forms import asset
from zabbix_manage.util import select_form_strTolist,Pager
from zabbix_manage.util import ip_validata
from ZabbixOp.settings import logger
import json
import traceback

zabbix = Zabbix()
host_group_type = [(group_info['GroupId'],group_info['GroupName'])
                   for group_info in zabbix.get_hostgroup() ]

template_type = [(template_info['TemplateId'],template_info['TemplateName'])
                 for template_info in zabbix.get_template()]

import sys
if sys.version_info[0] < 3 and sys.version_info <= 7:
    reload(sys)
    sys.setdefaultencoding('utf8')

@login_required(login_url='/login')
def index(request):
    if request.method == 'GET':
        zabbix = Zabbix()
        total_hostlist = zabbix.get_hostinfo()
        total_grouplist =zabbix.get_hostgroup()
        total_template = zabbix.get_template()
        total_host_num = len(total_hostlist)
        total_hostgroup_num = len(total_grouplist)
        total_template_num = len(total_template)

        ##分页
        current_page = request.GET.get('page',1)
        pager = Pager(current_page)
        views_hostlist = total_hostlist[pager.start:pager.end]

        pager_html = pager.pager_html(base_url="/",total_items=total_host_num)
    return render(request,'index.html',locals())

@login_required(login_url='/login')
def add_host(request):
    ret = {'model':asset.SampleForm(),'message':'','tips':'','tip_status':None}
    response = {'failed':[],
                'success':[]
                }
    if request.method == "POST":
        try:
            form = asset.SampleForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                print(data['ip'],data['hostname'],data['template'],data['hostgroup'])
                print('lalala')
                ##处理select插件返回的数据转换为列表
                data['hostgroup'] = select_form_strTolist(data['hostgroup'])
                data['template'] = select_form_strTolist(data['template'])
                data['ip'] = [ ip.strip() for ip in data['ip'].encode('utf-8').split('\n')]
                data['hostname'] = [ hostname.strip() for hostname in data['hostname'].encode('utf-8').split('\n')]
                print(data)
                result = zabbix.create_multi_host(host_list=data['ip'],
                                                  group_list=data['hostgroup'],
                                                  template_list=data['template'],
                                                  hostname_list=data['hostname'])
                print(request)
                if len(result['failed']) == 0:
                    hostid_list = [hostid['hostids'] for hostid in result['success']]
                    response['success'].extend(hostid_list)
                else:
                    response['failed'].extend(result['failed'])
                print(response)
                logger.info(str(response))
                return HttpResponse(json.dumps(response))
            else:
                ret['error'] = form.errors
                ret['model'] = form
                print(ret)
                return HttpResponse(json.dumps({'error':form.errors}))
        except Exception as e :
            traceback.print_exc()
    else:
        form = asset.SampleForm()
    return render(request,'add_host_monitor.html',ret)

def del_host(request):
    ret = {'result':None,'message':''}
    if request.method == 'POST':
        hostIps = request.POST.get('delete_ip',None)
        print(hostIps)
        try:
            if hostIps:
                hostIps = hostIps.split('\n')
                valid_ip = []
                for ip in hostIps:
                    if ip_validata(ip.strip()) == 'falied':
                        valid_ip.append(ip)
                if len(valid_ip) > 0:
                    ret['message'] = ','.join(valid_ip) + " 错误的IP地址"
                    ret['result'] = 'falied'
                    return HttpResponse(json.dumps(ret))
                else:
                    print(hostIps)
                    print('#' * 10)
                    del_result = zabbix.del_host(*hostIps)
                    ret['result'] = 'falied'
                    ret['message'] = del_result
                    logger.info(str(ret))
                    return HttpResponse(json.dumps(ret))
            else:
                ret['result'] = 'falied'
                ret['message'] = 'IP地址不能为空'
                return HttpResponse(json.dumps(ret))
        except Exception as e:
            traceback.print_exc()
    else:
        return HttpResponse('主机删除页面')


def zabbix_op(request):
    return render(request,'hostgroup.html',locals())

def zabbix_status(request):
    return HttpResponse('zabbix_status')

def zabbix_chart(request):
    return HttpResponse('zabbix_chart')

def account(request):
    return HttpResponse('account')

def account_login(request):
    login_err = ''
    if request.method == 'POST':
        email = request.POST.get('email','')
        password = request.POST.get('password','')
        user = authenticate(username=email,password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect('/')
        else:
            login_err = "密码或者邮箱错误,请重试!"
    return render(request,'login.html',locals())

def account_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))
