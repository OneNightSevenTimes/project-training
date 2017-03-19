#Author: Wang YiChen
#coding=utf-8

import re

class Pager(object):
    def __init__(self,current_page):
        self.current_page = int(current_page)

    @property
    def start(self):
        return (self.current_page - 1) * 10

    @property
    def end(self):
        return self.current_page * 10

    def pager_html(self,base_url,total_items):
        page_total,div = divmod(total_items,10)
        if div > 0:
            page_total += 1
        page_list = []  ##存放页码的html字符串

        ##默认显示6个页码
        # start = self.current_page - 5
        # end = self.current_page + 5
        ##智能点击页码,显示默认前后总共10条页码
        if page_total <= 6:
            start = 1
            end = page_total + 1 ##range(1,page_total+1)
            print(end)
        else:
            if self.current_page <= 3:
                start = 1
                end = 7
            else:
                start = self.current_page - 3
                end = self.current_page + 3
                if self.current_page + 3 > page_total:
                    start = page_total - 5
                    end = page_total + 1


        ##动态生成前端页码
        for page in  range(start,end):
            if self.current_page == page:  ##如果是当前页码,加红色便于识别
                temp = """<li><a style="color: #23527c;background-color: #eee;border-color: #ddd;" href="%s?page=%d">%d</a></li>""" %(base_url,page,page)
            else:
                temp = """<li><a href="%s?page=%d">%d</a></li>""" %(base_url,page,page)
            page_list.append(temp)
        ##上一页
        if self.current_page > 1:
            pre_page = """<li><a href="%s?page=%d" aria-label="上一页"><span aria-hidden="true">&laquo;</span></a></li>"""%(base_url,self.current_page - 1)
            #"""<a href="%s?page=%d">上一页</a>""" %(base_url,self.current_page - 1)

        else:
            pre_page = """<li><a href="javascript:void(0)" aria-label="上一页"><span aria-hidden="true">&laquo;</span></a></li>"""
        page_list.insert(0,pre_page)

        ##下一页
        if self.current_page >= page_total:
            next_page =  """<li><a href="javascript:void(0)" aria-label="上一页"><span aria-hidden="true">&raquo;</span></a></li>"""
            #"""<a href="javascript:void(0)">下一页</a>"""

        else:
            next_page =  """<li><a href="%s?page=%d" aria-label="上一页"><span aria-hidden="true">&raquo;</span></a></li>"""%(base_url,self.current_page + 1)
            #"""<a href="%s?page=%d">下一页</a>""" %(base_url,self.current_page + 1)
            print(self.current_page)
        page_list.append(next_page)
        ##首页
        home_page = """<li><a class="page" href="%s?page=%d">首页</a></li>""" %(base_url,1)
        page_list.insert(0,home_page)
        ##尾页
        end_page = """<li><a class="page" href="%s?page=%d">尾页</a></li>""" %(base_url,page_total)
        page_list.append(end_page)
        ###生成html字符串
        page_str = ''.join(page_list)
        return page_str


def select_form_strTolist(data):
    """
    django form表单select插件返回一个字符串形式的u"[u'1', u'2', u'4', u'5', u'6']"
    将其转换为[1,2,4,5,6]
    :param list: 列表里面str转换成Int
    :return:
    """
    data = eval(data)
    return [int(i) for i in data]


def ip_validata(ip):
    ip_re = re.compile(r'^((([1-9]?|1\d)\d|2([0-4]\d|5[0-5]))\.){3}(([1-9]?|1\d)\d|2([0-4]\d|5[0-5]))$')
    if not ip_re.match(ip):
        return 'falied'
    return 'success'

