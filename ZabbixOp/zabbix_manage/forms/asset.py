#coding=utf-8
from django import forms
from zabbix_manage.zabbix_api import Zabbix
from django.core.exceptions import ValidationError

import re


zabbix = Zabbix()
hostgroup = zabbix.get_hostgroup()
template= zabbix.get_template()

host_group_type = [
    (host_info['GroupId'],
                    host_info['GroupName']) for host_info in hostgroup
    ]
template_type = [
    (template_info['TemplateId'],
                  template_info['TemplateName']) for template_info in template
    ]

def mobile_validate(value):
    mobile_re = re.compile(r'^(13[0-9]|15[0-9]|17[678]|18[0-9]|14[5-7])[0-9]{8}$')
    if not mobile_re.match(value):
        raise ValidationError('手机号码格式错误')

def ip_validata(value):
    ip_list = [ ip.strip() for ip in value.split('\n')]
    ip_re = re.compile(r'^((([1-9]?|1\d)\d|2([0-4]\d|5[0-5]))\.){3}(([1-9]?|1\d)\d|2([0-4]\d|5[0-5]))$')
    print(value)
    valid_ip = []
    for ip in ip_list:
        if not ip_re.match(ip):
            valid_ip.append(ip)
    if len(valid_ip) > 0:
        valid_data = ','.join(valid_ip)
        raise ValidationError('什么玩意儿IP地址:'+ valid_data)


class SampleAddHost(forms.Form):
    pass

class NameForm(forms.Form):
    your_name = forms.CharField(label="Your Name",max_length=100)

class ContackForm(forms.Form):
    Host = forms.CharField(max_length=100,widget=forms.Textarea)
    HostGroup = forms.CharField(max_length=100)
    Template = forms.EmailField()
    mail = forms.BooleanField(required=False)

class SampleForm(forms.Form):
    hostname = forms.CharField(required=False,
                               error_messages={'required':u'主机名不能为空',u'invalid':u'主机格式错误'},
                               widget=forms.Textarea(attrs={'class':'form-control no-radius',
                                                            'placeholder':u'多个主机名,请按行隔开',
                                                            'id':'hosts',
                                                            'cols':42,'rows':5,'value':'test'}))
    ip = forms.CharField(validators=[ip_validata,],
                         error_messages={'required':u'ip地址不能为空',u'invalid':u'格式必须是一个ip地址'},
                         widget=forms.Textarea(attrs={'class':'form-control no-radius',
                                                      'id':'ips',
                                                       'placeholder':u'多个IP地址,请按行隔开',
                                                       'cols': '42', 'rows': '5'}),)
    hostgroup = forms.CharField(error_messages={'required':u'主机组不能为空'},
                                widget=forms.SelectMultiple(choices=host_group_type,
                                                    attrs={"class":'form-control no-radius',
                                                           "id":'hostgroups',
                                                           'size':10}))
    template = forms.CharField(error_messages={'required':u'Template不能为空'},
                               widget=forms.SelectMultiple(choices=template_type,
                                                    attrs={'class':'form-control no-radius',
                                                           'id':'templates',
                                                            'size':10}))
    def __init__(self,*args,**kwargs):
        super(SampleForm,self).__init__(*args,**kwargs)


